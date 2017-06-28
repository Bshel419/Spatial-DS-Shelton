import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/airports.json', 'r')

data = f.read()

data = json.loads(data)

airports = []


for k,v in data.items():
    if(len(airports) < 1000):
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = v
        lat = v['lat']
        lon = v['lon']
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
            lon,
            lat
        ]
        airports.append(gj)
    
    
out = open(DIRPATH + '/geo_json/airports_gj.geojson', 'w')

out.write(json.dumps(airports, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()

