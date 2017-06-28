import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/world_cities_large.json', 'r')

data = f.read()

data = json.loads(data)

cities = []


for k,v in data.items():
    for item in v:
        if(len(cities) < 1000):
            gj = collections.OrderedDict()
            gj['type'] = "Feature"
            gj['properties'] = item
            lat = float(item['lat'])
            lon = float(item['lon'])
            del gj['properties']['lat']
            del gj['properties']['lon']
            gj["geometry"] = {}
            gj["geometry"]["type"]="Point"
            gj["geometry"]["coordinates"] = [
                lon,
                lat
            ]
            cities.append(gj)
    
    
out = open(DIRPATH + '/geo_json/city_locations_gj.geojson', 'w')

out.write(json.dumps(cities, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()