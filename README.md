# django_morocco_mapping

this app offers Administrative Boundaries splitting of the Moroccan Kingdom. 

data has been mined through http://overpass-turbo.eu/ and fixed (some polygons were corrupted).


requirements to install using pip: 
tqdm
wget

Add the following variables to your settings file:
regions= الجهات
wilayas=الأقاليم أو العمالة 
subregion= الباشوية أو الدائرة 
commune= الجماعة الحضارية أو القروية 
place=   مدينة أو قرية أو ضاحية أو بلدة أو بلدية 
place is in the form of point unfortunately 
MAPPING_FILES_URI = {
    'country':{'filename':"morocco.geojson",
              'filelink':""},
    'region':{'filename':"regions.geojson",
              'filelink':"https://gdurl.com/Te8W"},
    'wilaya':{'filename':"wilayas.geojson",
              'filelink':"https://gdurl.com/ARwV"} ,
    'subregion':{'filename':"subregions.geojson",
                  'filelink':"https://gdurl.com/I0SL"},
    'commune':{'filename':"communes.geojson",
                'filelink':"https://gdurl.com/GWNl"},
    'place':{'filename':"places.geojson",
             'filelink':"https://gdurl.com/TLYg"},
}
replace /// with the dict {'filename':FILENAME,'filelink':DIRECT_LINK_TO_FILE}
######################
a directory to use temporarily for downloading files
MAPPING_TEMP_DIR = '/var/tmp'

localies for alternative names assignement
MAPPING_LOCALIES = ['en', 'ar', 'fr']
