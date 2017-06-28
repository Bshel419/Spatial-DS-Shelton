import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__))

f = open(DIRPATH + '/countries.json', 'r')

data = f.read()

data = json.loads(data)

countries = []

for k in data:
    if(len(countries) < 1000):
        countries.append(k) 

out = open(DIRPATH + '/geo_json/countries_gj.geojson', 'w')

out.write(json.dumps(countries, sort_keys = False, indent = 4, separators=(',', ': ')))

out.close()