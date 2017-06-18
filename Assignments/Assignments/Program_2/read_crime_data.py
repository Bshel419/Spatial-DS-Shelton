import pprint as pp
import os,sys

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

keys = []
crimes = []
crimePoints = []

got_keys = False
#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:
with open(DIRPATH+'/'+'Nypd_Crime_01.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue

        #d = {}
        # for i in range(len(line)-1):
        #     d[keys[i]] = line[i]
        crimes.append(line)
#for crime in crimes:
    #print(crime[19],crime[20])

for crime in crimes:
    if crime[21] == '':
        continue
    else:
        x = crime[21]
    if crime[22] == '':
        continue
    else:
        y = crime[22]

    crimePoints.append((x,y))