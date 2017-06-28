import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/earthquakes-1960-2017.json', 'r')

data = f.read()

data = json.loads(data)

earthquakes = []

itterator = int(0)

for k,v in data.items():
    for item in v:
        if(itterator < 1000):
            gj = collections.OrderedDict()
            gj['type'] = "Feature"
            gj['properties'] = item
            lat = item['geometry']['coordinates'][0]
            lon = item['geometry']['coordinates'][1]
            del gj['properties']['geometry']
            gj["geometry"] = {}
            gj["geometry"]["type"]="Point"
            gj["geometry"]["coordinates"] = [
                lon,
                lat
            ]
            earthquakes.append(gj)
            itterator += 1

out = open(DIRPATH + '/geo_json/earthquakes_gj.geojson', 'w')

out.write(json.dumps(earthquakes, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()