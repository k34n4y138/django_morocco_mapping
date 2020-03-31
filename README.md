
# django_morocco_mapping V0.1

this app offers Administrative Boundaries splitting of the Moroccan Kingdom. 
data has been mined through http://overpass-turbo.eu/ and fixed (some polygons were corrupted).

# requirements to install using pip: 
tqdm
wget

# Add the following variables to your settings file:
'INSTALLED_APPS=[
...
'morocco_mapping'
...
]'

`MAPPING_FILES_URI = {
    'country':{'filename':"morocco.geojson",
              'filelink':"https://gdurl.com/Ap2w"},
    'region':{'filename':"regions.geojson",
              'filelink':"https://gdurl.com/Te8W"},
    'wilaya':{'filename':"wilayas.geojson",
              'filelink':"https://gdurl.com/ARwV"} ,
    'subregion':{'filename':"subregions.geojson",
                  'filelink':"https://gdurl.com/I0SL"},
    'commune':{'filename':"communes.geojson",
                'filelink':"https://gdurl.com/GWNl"},
    'place':{'filename':"places.geojson",
             'filelink':"https://gdurl.com/TLYg"}
}`
<br/>
#### a directory to use temporarily for downloading files
`MAPPING_TEMP_DIR = '/var/tmp`
<br/>
#### localies for alternative names assignement
`MAPPING_LOCALIES = ['en', 'ar', 'fr']`

# Initiation:
after making sure the settings above are all set 
open the terminal at your project directory and execute the following:
`python manage.py migrate morocco_mapping`

#### db population:
make sure the files above are pointing to the right files and none is missing 
`python manage.py morocco_mapping`


## TODOS:
-add serializers and APIViews so to allow external retrievement
