import io
import json
import os
from time import sleep

import wget
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from bimaristarAPI import settings
from bimaristarAPI.apps.geostuff.morocco_mapping.models import Country, Region, Wilaya, Subregion, Commune, \
    BoundaryCenter, Place


class Command(BaseCommand):
    def tell(self, text):
        self.stdout.write(self.style.SUCCESS(text))
        sleep(0.5)

    @transaction.atomic
    def handle(self, *args, **options):
        self.tell('Initiating')

        if not os.path.exists(self.TEMP_DIR):
            self.tell('creating %s for temp usage' % self.TEMP_DIR)
            os.makedirs(self.TEMP_DIR)
        for key in self.TERRITORY_MODEL.keys():
            self.load_territory(key)
        self.load_places()
        self.tell('DONE!')
        self.final_clean()

    def is_feature(self, geoproperties, feature):
        ft_type, ft_id = str(geoproperties.get("@id")).split('/')
        return bool(ft_type == feature)

    def is_center(self, geoproperties, parent):
        is_child = next((elem for elem in geoproperties['@relations'] if elem['rel'] == int(parent)), False)

        return bool(is_child)

    FILES_URI = settings.MAPPING_FILES_URI
    TEMP_DIR = getattr(settings, "MAPPING_TEMP_DIR", "/var/tmp/")
    LOCALIES = ['ar', 'en', 'fr']

    TERRITORY_MODEL = {
        'country': Country,
        'region': Region,
        'wilaya': Wilaya,
        'subregion': Subregion,
        'commune': Commune
    }
    TERRITORY_PARENT = {
        'country': None,
        'region': Country,
        'wilaya': Region,
        'subregion': Wilaya,
        'commune': Subregion
    }
    T_P_KEY = {
        'country': None,
        'region': "country",
        'wilaya': "region",
        'subregion': "wilaya",
        'commune': "subregion"
    }
    TERRITORY_TYPES = {
        'wilaya': {'prefecture': 1,
                   'province': 2},
        'subregion': {'cercle': 1,
                      'pachalik': 2}
    }

    def file_download(self, territory):
        self.tell('Downloading %s' % territory)
        sleep(0.2)
        target = self.FILES_URI[territory]
        url = target['filelink']  # big file test
        dest = os.path.join(self.TEMP_DIR, target['filename'])
        # Streaming, so we can iterate over the response.
        if os.path.exists(dest):
            os.remove(dest)
        wget.download(url, dest, bar=wget.bar_adaptive)
        self.tell(' Finished Download.')

    def get_data(self, territory):
        target = self.FILES_URI[territory]
        target_dir = os.path.join(self.TEMP_DIR, target['filename'])
        file_obj = io.open(target_dir, encoding='utf-8')
        # should be a list data
        return dict(json.load(file_obj))

    def final_clean(self):
        self.tell('performing cleanup for temp files')
        for tkey in tqdm(self.FILES_URI.keys(), total=len(self.FILES_URI), desc='deleting files '):
            target = self.FILES_URI[tkey]
            target_dir = os.path.join(self.TEMP_DIR, target['filename'])
            if os.path.exists(target_dir):
                os.remove(target_dir)

    def assign_alt_names(self, obj, feature_properties):
        ft_alt_names = {}
        for loc in self.LOCALIES:
            ft_alt_names.update({
                loc: feature_properties.get('name:' + loc, None)
            })
        for loc in ft_alt_names.keys():
            if ft_alt_names[loc] is not None:
                obj.alt_name.create(lang=loc,
                                    name=ft_alt_names[loc])
        obj.save()

    def load_territory(self, territory):
        self.file_download(territory)
        features_list = self.get_data(territory)['features']
        nodes = list(
            (elem for elem in features_list if self.is_feature(elem["properties"], feature='node')))
        relations = list((elem for elem in features_list if self.is_feature(elem["properties"], feature='relation')))
        for feature in tqdm(relations, desc='Loading ' + territory, total=len(relations)):
            creation_params = {}
            ft_properties = feature.get('properties')
            ft_type, ft_id = str(ft_properties.get("@id")).split('/')
            try:
                ft_geometry = GEOSGeometry(str(feature.get('geometry')))
            except:
                raise Exception('the geometry of feature %s is corrupted' % ft_id)
            if ft_geometry and isinstance(ft_geometry, geos.Polygon):
                ft_geometry = geos.MultiPolygon(ft_geometry)

            center_node = next((elem for elem in list(nodes) if self.is_center(elem['properties'], parent=ft_id)), None)
            if center_node is not None:
                center_geometry = GEOSGeometry(str(center_node['geometry']))
                center_id = str(center_node.get('id')).split('/')[1]
                center_obj = BoundaryCenter.objects.create(osm_id=center_id, point=center_geometry)
                creation_params.update({'center': center_obj})
            creation_params.update({'osm_id': ft_id,
                                    'name': ft_properties.get('name', None),
                                    'shape': ft_geometry,
                                    'wikidata': ft_properties.get('wikidata', None)})

            if territory in self.TERRITORY_TYPES.keys():
                ft_network = str(ft_properties.get('network')).lower()
                for key in self.TERRITORY_TYPES[territory].keys():
                    if key in ft_network:
                        creation_params.update({
                            territory + '_type': self.TERRITORY_TYPES[territory][key]
                        })

            if self.TERRITORY_PARENT[territory] is not None:
                try:
                    parent = self.TERRITORY_PARENT[territory].objects.filter(shape__contains=center_geometry)[0]
                    creation_params.update({self.T_P_KEY[territory]: parent})
                except:
                    parent = self.TERRITORY_PARENT[territory].objects.filter(shape__contains=ft_geometry)[0]
                    creation_params.update({self.T_P_KEY[territory]: parent})

            territory_obj, created = self.TERRITORY_MODEL[territory].objects.get_or_create(**creation_params)
            self.assign_alt_names(territory_obj, ft_properties)
            territory_obj.save()

    def load_places(self):
        self.file_download('place')
        features_list = self.get_data('place')['features']
        places = list((elem for elem in features_list if (self.is_feature(elem["properties"], feature='node'))))

        for feature in tqdm(places, 'loading places', total=len(places)):
            ft_properties = feature.get('properties')
            ft_name = ft_properties.get('name', None)
            ft_type, ft_id = str(ft_properties.get("@id")).split('/')
            ft_geometry = GEOSGeometry(str(feature.get('geometry')))
            ft_place = ft_properties.get('place')
            try:
                parent = Commune.objects.filter(shape__contains=ft_geometry)[0]
            except Commune.DoesNotExist:
                raise Exception('object %s does not have a parent' % ft_id)
            place_obj = Place.objects.create(osm_id=ft_id,
                                             name=ft_name,
                                             place_type=ft_place,
                                             commune=parent,
                                             point=ft_geometry,
                                             )
            self.assign_alt_names(place_obj, ft_properties)
            place_obj.save()
