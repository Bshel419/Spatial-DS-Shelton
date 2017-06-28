import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/state_borders.json', 'r')

data = f.read()

data = json.loads(data)

states = []


for k in data:
    if(len(states) < 1000):
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = k
        gj["geometry"] = {}
        gj["geometry"]["type"]="MultiPolygon"
        gj['geometry']['coordinates'] = [gj['properties']['borders']]
        del gj['properties']['borders']
        states.append(gj)
    
    
out = open(DIRPATH + '/geo_json/states_gj.geojson', 'w')

out.write(json.dumps(states, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()

