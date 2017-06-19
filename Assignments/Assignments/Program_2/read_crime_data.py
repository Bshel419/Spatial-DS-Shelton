import pprint as pp
import os,sys

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

keys = []
#original file data for all 5 burrows
bronx_crimes = []
brooklyn_crimes = []
manhattan_crimes = []
manhattan_crimes = []
queens_crimes = []
staten_island_crimes = []

#just the x,y coordinates for the 5 burrows
bronx_crimePoints = []
brooklyn_crimePoints = []
manhattan_crimePoints = []
queens_crimePoints = []
staten_island_crimePoints = []

#get all the data
got_keys = False
#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:
with open(DIRPATH+'/'+'filtered_crimes_bronx.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue
        bronx_crimes.append(line)

with open(DIRPATH+'/'+'filtered_crimes_brooklyn.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue

        brooklyn_crimes.append(line)

with open(DIRPATH+'/'+'filtered_crimes_manhattan.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue

        manhattan_crimes.append(line)
    
with open(DIRPATH+'/'+'filtered_crimes_queens.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue
            
        queens_crimes.append(line)

with open(DIRPATH+'/'+'filtered_crimes_staten_island.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue
            
        staten_island_crimes.append(line)

#now do some type casting and get the x,y coordinates stored into the crimePoints list
for crime in bronx_crimes:
    if(len(crime) == 24):
        if crime[19] == '':
            continue
        else:
            x = int(crime[19])
            newX = x
        if crime[20] == '':
            continue
        else:
            y = int(crime[20])
            newY = y

        bronx_crimePoints.append((newX,newY))

for crime in brooklyn_crimes:
    if(len(crime) == 24):
        if crime[19] == '':
            continue
        else:
            x = int(crime[19])
            newX = x
        if crime[20] == '':
            continue
        else:
            y = int(crime[20])
            newY = y

        brooklyn_crimePoints.append((newX,newY))

for crime in manhattan_crimes:
    if(len(crime) == 24):
        if crime[19] == '':
            continue
        else:
            x = int(crime[19])
            newX = x
        if crime[20] == '':
            continue
        else:
            y = int(crime[20])
            newY = y

        manhattan_crimePoints.append((newX,newY))

for crime in queens_crimes:
    if(len(crime) == 24):
        if crime[19] == '':
            continue
        else:
            x = int(crime[19])
            newX = x
        if crime[20] == '':
            continue
        else:
            y = int(crime[20])
            newY = y

        queens_crimePoints.append((newX,newY))

for crime in staten_island_crimes:
    if(len(crime) == 24):
        if crime[19] == '':
            continue
        else:
            x = int(crime[19])
            newX = x
        if crime[20] == '':
            continue
        else:
            y = int(crime[20])
            newY = y

        staten_island_crimePoints.append((newX,newY))
    