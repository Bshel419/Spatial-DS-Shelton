import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
from read_crime_data import *


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)


DIRPATH = os.path.dirname(os.path.realpath(__file__))
background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (2000,2000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Line')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 20
min_pts = 5.0

bronx_points = []
brooklyn_points = []
manhattan_points = []
queens_points = []
staten_island_points = []

bronx_adjustedPoints = []
brooklyn_adjustedPoints = []
manhattan_adjustedPoints = []
queens_adjustedPoints = []
staten_island_adjustedPoints = []

for x,y in bronx_crimePoints:
    bronx_points.append((x,y))

for x,y in brooklyn_crimePoints:
    brooklyn_points.append((x,y))

for x,y in manhattan_crimePoints:
    manhattan_points.append((x,y))

for x,y in queens_crimePoints:
    queens_points.append((x,y))

for x,y in staten_island_crimePoints:
    staten_island_points.append((x,y))


# maxx = float(1067226) # The max coords from the 
# maxy = float(271820)  # whole file
# minx = float(913357)
# miny = float(121250)
# deltax = float(maxx) - float(minx)
# deltay = float(maxy) - float(miny)

# for p in loc_data['points']:
#     x,y = p['xy']
#     x = float(x)
#     y = float(y)
#     xprime = (x - minx) / deltax         # val (0,1)
#     yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
#     p['adjusted'] = (xprime,yprime) 

maxx = float(1067226) # The max coords from the 
maxy = float(271820)  # whole file
minx = float(913357)
miny = float(121250)
deltax = float(maxx) - float(minx)
deltay = float(maxy) - float(miny)

for x,y in bronx_points:
    x = float(x)
    y = 1 - float(y)
    newX = (x - minx)/deltax
    newY = (y - miny)/deltay
    newX = int(newX * 1000)
    newY = int(newY * 1000)
    bronx_adjustedPoints.append((newX ,newY))

for x,y in brooklyn_points:
    x = float(x)
    y = 1 - float(y)
    newX = (x - minx)/deltax
    newY = (y - miny)/deltay
    newX = int(newX * 1000)
    newY = int(newY * 1000)
    brooklyn_adjustedPoints.append((newX ,newY))

for x,y in manhattan_points:
    x = float(x)
    y = 1 - float(y)
    newX = (x - minx)/deltax
    newY = (y - miny)/deltay
    newX = int(newX * 1000)
    newY = int(newY * 1000)
    manhattan_adjustedPoints.append((newX ,newY))

for x,y in queens_points:
    x = float(x)
    y = 1 - float(y)
    newX = (x - minx)/deltax
    newY = (y - miny)/deltay
    newX = int(newX * 1000)
    newY = int(newY * 1000)
    queens_adjustedPoints.append((newX ,newY))

for x,y in staten_island_points:
    x = float(x)
    y = 1 - float(y)
    newX = (x - minx)/deltax
    newY = (y - miny)/deltay
    newX = int(newX * 1000)
    newY = int(newY * 1000)
    staten_island_adjustedPoints.append((newX ,newY))


running = True
while running:

    for p in bronx_adjustedPoints:
        pygame.draw.circle(screen, black, p, 3, 0)
    for p in brooklyn_adjustedPoints:
        pygame.draw.circle(screen, black, p, 3, 0)
    for p in manhattan_adjustedPoints:
        pygame.draw.circle(screen, black, p, 3, 0)
    for p in queens_adjustedPoints:
        pygame.draw.circle(screen, black, p, 3, 0)
    for p in staten_island_adjustedPoints:
        pygame.draw.circle(screen, black, p, 3, 0)
    #for mbr in mbrs:
        #pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        #pygame.image.save(screen, DIRPATH+'/'+"NY_Screenshot.png")
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #clean_area(screen,(0,0),width,height,(255,255,255))
            #adjustedPoints.append(event.pos)
           # mbrs = calculate_mbrs(adjustedPoints, epsilon, min_pts)
    pygame.display.flip()