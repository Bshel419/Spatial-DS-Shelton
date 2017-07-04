from mongo_helper import *
from map_helper import *
import pprint as pp
import sys
import pygame


DIRPATH = os.path.dirname(os.path.realpath(__file__))

#display stuff
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024,512)
color_list = {'volcanos':(255,0,0),'earthquakes':(0,0,255),'meteorites':(0,255,0)}

#pygame stuff
pygame.init()
bg = pygame.image.load(DIRPATH+'/draw_world_map/images/1024x512.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query2: Nearest Neighbor')
screen.fill(background_colour)
pygame.display.flip()

#initialize variables
feature = None
field = None
field_value = None
min_max = None
max_results = None
radius = None
lat,lon = (None,None)

#if you used the command line for variable input
if(len(sys.argv)==1):
    radius = 200
    max_results = 100
#radius and max results
elif(len(sys.argv)>1 and (len(sys.argv))<3):
    radius = float(sys.argv[1])
    max_results = 100
#everything is passed
elif(len(sys.argv)>3):
    
    feature = sys.argv[1]
    field = sys.argv[2]
    field_value = float(sys.argv[3])
    min_max = sys.argv[4]
    max_results = int(sys.argv[5])
    radius = float(sys.argv[6])
    #if a lat,lon is passed 
    if(len(sys.argv) > 7):
        lat,lon = eval(sys.argv[7])

#running loop stuff
x_y_coords = None
result_list = []
res = []
feature_list = ['volcanos','earthquakes','meteorites']

#lists to hold x,y conversions along with lat lon conversions
allx = []
ally = []
points = []
extremes = {}
adj = {}


picked_pt = False
if(len(sys.argv))>7:
    picked_pt = True
converted_to_lat_lon = False
find_feature = True
drawn = False

#display background
screen.blit(bg, (0, 0))
pygame.display.flip()

mh = MongoHelper()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and (len(sys.argv) < 3) and picked_pt == False:
            x_y_coords = (event.pos[0],event.pos[1])
            picked_pt = True
    
    #convert x_y_coords to lat,lon for mongodb
    if x_y_coords != None and converted_to_lat_lon == False:
        lon,lat = (event.pos[0],event.pos[1])
        lat = y_to_lat(lat,height)
        lon = x_to_lon(lon,width)
        converted_to_lat_lon = True

    #finds all the features
    if picked_pt == True and find_feature == True:
        #if no feature was chosen
        if feature == None:
            adj = {'volcanos':None,'earthquakes':None,'meteorites':None}
            for f in feature_list:
                result_list = mh.get_features_near_me(f,(lon,lat),radius)
                
                extremes,points = find_extremes(result_list, width, height)

                adj[f] = (adjust_location_coords(extremes,points,width,height))
                
                
        else:
            #if a feature was chosen
            result_list = mh.get_features_near_me(feature,(lon,lat),radius)
            adj = {feature: None}
            for r in result_list:
                if min_max == 'min':
                    if float(r['properties'][field]) > field_value:
                        res.append(r)
                if min_max == 'max':
                    if r['properties.'+field] < field_value:
                        res.append(r)
            result_list = []
            
            #narrrows results down
            for f in range(max_results):
                result_list.append(res[f])

            extremes,points = find_extremes(result_list, width, height)

            adj[feature] = (adjust_location_coords(extremes,points,width,height))

        find_feature = False

    #prints all pts
    if picked_pt == True and drawn == False:
        for f in adj.keys():
            for pt in adj[f]:
                pygame.draw.circle(screen, color_list[f], pt, 2,0)
                pygame.display.flip()
        #saves the image
        pygame.image.save(screen, DIRPATH+'/query2.png')