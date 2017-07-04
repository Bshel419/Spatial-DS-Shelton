"""
Program:
--------
    Program 5 - query3 : Clustering
Description:
------------
    See README
    
Name: Chris W Cook
Date: 05 July 2017
"""
from mongo_helper import *
from map_helper import *
from dbscan import *
import pprint as pp
import pygame
import sys,os

DIRPATH = os.path.dirname(os.path.realpath(__file__))

#display
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1024, 512)
color_list = {'volcanos':(255,0,0),'earthquakes':(70,173,212),'meteorites':(76,187,23)}
box_color = (255,255,0)

#pygame stuff
pygame.init()
bg = pygame.image.load(DIRPATH+'/draw_world_map/images/1024x512.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('query3: Clustering')
screen.fill(background_colour)
pygame.display.flip()

#separate sys.argv
feature = sys.argv[1]
min_pts = float(sys.argv[2])
eps = float(sys.argv[3])


res = []
points = []
extremes = {}

#finds all features in world_data
result_list = mh.client['world_data'][feature].find()

extremes, points = find_extremes(result_list, width, height)

points = adjust_location_coords(extremes,points,width,height)

mbrs = calculate_mbrs(points, eps, min_pts)

#displays the pygame window with the background
screen.blit(bg, (0, 0))
pygame.display.flip()

#this is used to access the mongo db
mh = MongoHelper()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #draws all pts
    for mbr in mbrs:
         pygame.draw.polygon(screen, box_color, mbr, 2)
         pygame.display.flip()
    for pt in points:
        pygame.draw.circle(screen, color_list[feature], pt, 2,1)
        pygame.display.flip()
        #saves the image
    pygame.image.save(screen, DIRPATH+'/query3.png')