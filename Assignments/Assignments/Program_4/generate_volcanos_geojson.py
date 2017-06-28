import pprint as pp
import os,sys
import json
import collections
import decimal 

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/world_volcanos.json', 'r')

data = f.read()

data = json.loads(data)

volcanos = []


for k in data:
    if(len(volcanos) < 1000  and not(k['Lat'] == '')):
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = k
        lat = float(k['Lat'])
        lon = float(k['Lon'])
        del gj['properties']['Lat']
        del gj['properties']['Lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
            lon,
            lat
        ]
        volcanos.append(gj)
    
    
out = open(DIRPATH + '/geo_json/volcanos_gj.geojson', 'w')

out.write(json.dumps(volcanos, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()