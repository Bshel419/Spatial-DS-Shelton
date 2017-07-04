from mongo_helper import *
from map_helper import *
from dbscan import *
import pygame
import pprint as pp
import sys,os

#path
DIRPATH = os.path.dirname(os.path.realpath(__file__))
#connection to mongoDB
mh = MongoHelper()

#lists that hold stuff
extremes = {}
points = []

#5 largest bounding rectangles
finalBRs = []

#screen and color stuff
background_color = (255,255,255)
black = (0,0,0)
(width,height) = (1024,512)
color_list = {'volcanos':(255,0,0),'earthquakes':(0,0,255),'meteorites':(0,255,0)}
rect_color = (0,255,0)

#pygame stuff
pygame.init()
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load(DIRPATH+'/draw_world_map/images/1024x512.png')
screen.fill(background_color)
pygame.display.flip()

#grab the 3 determining variables from the command line
feature = sys.argv[1]
min_pts = float(sys.argv[2])
eps = float(sys.argv[3])

#add background image
screen.blit(bg, (0,0))
pygame.display.flip()

#process data to find minimum bounding rectangles
feature_list = mh.client['world_data'][feature].find()

extremes,points = find_extremes(feature_list, width, height)

points = adjust_location_coords(extremes,points,width,height)

mbrs = calculate_mbrs(points, eps, min_pts)

#sort the list of mbrs(largest-smallest in length)
sorted(mbrs, key=len) 

#add 5 largest to finalBRs
for x in range(0,5):
    finalBRs.append(mbrs[x])

#print all the good stuff
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for rec in finalBRs:
        pygame.draw.polygon(screen,rect_color,rec,2)
        pygame.display.flip()
    for p in points:
        pygame.draw.circle(screen, color_list[feature], p, 2,1)
        pygame.display.flip()
    
    #saves image
    pygame.image.save(screen, DIRPATH+'/query3.png')


