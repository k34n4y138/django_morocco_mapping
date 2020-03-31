# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models

from bimaristarAPI.apps.core.models import TimestampedModel


class AlternativeName(TimestampedModel):
    lang = models.CharField(max_length=5, default='und')
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    place = GenericForeignKey()


class BaseLocation(TimestampedModel):
    name = models.CharField(max_length=255, null=True)
    osm_id = models.BigIntegerField()
    wikidata = models.CharField(max_length=50, null=True)
    alt_name = GenericRelation(AlternativeName)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BasePoint(BaseLocation):
    point = models.PointField()

    class Meta:
        abstract = True


class BoundaryCenter(BasePoint):
    pass


class BaseBoundary(BaseLocation):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField()
    shape = models.MultiPolygonField()
    center = models.OneToOneField(BoundaryCenter, on_delete=models.PROTECT, null=True)

    class Meta:
        abstract = True


class Country(BaseBoundary):
    pass


class Region(BaseBoundary):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='regions')


class Wilaya(BaseBoundary):
    WILAYAS = (
        (1, 'Prefecture'),
        (2, 'Province')
    )

    osm_id = models.BigIntegerField()
    wilaya_type = models.PositiveSmallIntegerField(choices=WILAYAS, default=2)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='Wilayas')


class Subregion(BaseBoundary):
    SUBREGIONS = (
        (1, 'Cercle'),
        (2, 'Pachalik')
    )
    subregion_type = models.PositiveSmallIntegerField(choices=SUBREGIONS, default=2)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT, related_name='subregions')


class Commune(BaseBoundary):
    subregion = models.ForeignKey(Subregion, on_delete=models.PROTECT, related_name='communes')


class Place(BasePoint):
    # village
    # city
    # town
    # municipality
    # suburb
    place_type = models.CharField(max_length=50)
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT, related_name='places')
