import os,sys
import math



def get_extremes(points):
    maxX = -999
    minX = 999
    maxY = -999
    minY = 999


# http://wiki.openstreetmap.org/wiki/Mercator
def merc_xy(lon,lat):
    #x portion
    r_major=6378137.000
    x = r_major*math.radians(lon)

    #y portion
    if lat>89.5:lat=89.5
    if lat<-89.5:lat=-89.5
    r_major=6378137.000
    r_minor=6356752.3142
    temp=r_minor/r_major
    eccent=math.sqrt(1-temp**2)
    phi=math.radians(lat)
    sinphi=math.sin(phi)
    con=eccent*sinphi
    com=eccent/2
    con=((1.0-con)/(1.0+con))**com
    ts=math.tan((math.pi/2-phi)/2)/con
    y=0-r_major*math.log(ts)
    return (x,y)

def find_extremes(result_list,width,height):
    '''
    find the extremes in a set of points.
    input:
        result_list: a list geojson entries
    '''
    extremes={}
    allx = []
    ally = []
    points = []
    for r in result_list:
        lon = r['geometry']['coordinates'][0]
        lat = r['geometry']['coordinates'][1]
        x,y = (mercX(lon),mercY(lat))
        allx.append(x)
        ally.append(y)
        points.append((x,y))
    '''   
    extremes['max_x'] = max(allx)
    extremes['min_x'] = min(allx)
    extremes['max_y'] = max(ally)
    extremes['min_y'] = min(ally)
    '''
    extremes['max_x'] = width
    extremes['min_x'] = 0
    extremes['max_y'] = height
    extremes['min_y'] = 0
    
    
    return extremes,points

def mercXY(lon,lat):
    r = 6378137
    scale = math.cos(lat * math.pi / 180.0)
    x = scale * lon * math.pi * r / 180.0
    y = scale * r * math.log( math.tan((90.0+lat) * math.pi / 360.0) )
    return (x,y)

def mercX(lon,zoom = 1):
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)

def adjust_location_coords(extremes,points,width,height):
    """
    Adjust your point data to fit in the screen. 
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxx = float(extremes['max_x']) # The max coords from bounding rectangles
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = []

    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay) # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)-256
        adjusted.append((adjx,adjy))
    return adjusted

def flatten_country_polygons(geometry):
    adjusted_polys = []
    if geometry['type'] == 'Polygon':
        pass
    else:
        for polygons in geometry['coordinates']:
            for polygon in polygons:
                newp = []
                for p in polygon:
                    newp.append([mercX(p[0]),mercY(p[1])])
                adjusted_polys.append(newp)
        return adjusted_polys

def mercToLL(point):
    lng,lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)

def x_to_lon(x,width):
    #http://board.flashkit.com/board/showthread.php?666832-Turn-latitude-longitude-into-X-Y-coordinates
    '''DEGREES_PER_RADIAN = 57.2958
    RADIANS_PER_DEGREE = 0.0174533
    sign = math.sin(x)
    sin = math.sin(x * RADIANS_PER_DEGREE * sign)
    #return (sign * (math.log((1.0 + sin) / (1.0 - sin)) / 2.0)) *180
    return (math.atan(math.sinh(float(x))) * DEGREES_PER_RADIAN);'''
    return ((float(x)/(width/360.0))-180.0)


def y_to_lat(y,height):
    #https://stackoverflow.com/questions/1166059/how-can-i-get-latitude-longitude-from-x-y-on-a-mercator-map-jpeg
    return ((((height/2.0)-y)/(height/2.0))*90)