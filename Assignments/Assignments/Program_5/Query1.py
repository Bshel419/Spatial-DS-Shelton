import os,sys
import math
from pymongo import MongoClient
import pygame
import map_helper as mapH

class MongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
        """
        x,y = point

        res = self.client['world_data'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )

        return self._make_result_list(res)

    def get_doc_by_keyword(self,collection,field_name,search_key,like=True):
        """
        Finds "documents" with some keyword in some field.
        Params:
            collection_name: e.g airports or meteors etc.
            field_name: key name of the field to search. e.g. 'place_id' or 'magnitude' 
            search_key: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_doc_by_keyword('earthquakes','properties.type','shakemap')
            # Returns all earthquakes that have the word 'shakemap' somewhere in the 'type' field
        """
        if like:
            # This finds the records in which the field just "contains" the search_key
            res = self.client['world_data'][collection].find(({field_name : {'$regex' : ".*"+search_key+".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['world_data'][collection].find({field_name : search_key})

        return self._make_result_list(res)


    def get_feature_in_poly(self,collection,poly):
        """
        Get features that are "in" a polygon
        Params:
            collection_name: e.g airports or meteors etc.
            poly: geojson polygon
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_feature_in_poly('airports',country['coordinates'])
            # Returns all airports in the given country polygon.
        """
        res = self.client['world_data'][collection].find( { 'geometry' : { '$geoWithin' : { '$geometry' : {'type': "Polygon", 'coordinates': poly }} } })

        return self._make_result_list(res)

    def get_poly_by_point(self,collection,point):
        """
        Get a polygon that a point is within
        Params:
            collection_name: e.g airports or meteors etc.
            point: geojson point
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
            # Returns the country that point([44.2968750,24.6669864]) is within (Saudi Arabia)
        """
        return self.client['world_data'][collection].find_one({'geometry':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_state_poly(self,state):
        """
        Send in a state name (e.g. Texas) or code (e.g. tx) and it returns the geometry
        """
        state = state.lower()
        if len(state) == 2:
            field = 'properties.code'
        else:
            state = state.capitalize()
            field = 'properties.name'

        state_poly = self.client['world_data']['states'].find_one({field : state})
        return state_poly['geometry']

    def get_country_poly(self,key):
        """
        Send in a country name (e.g. Belarus) or code (e.g. BLR) and it returns the geometry
        """
        country_poly = None
        if len(key) == 3:
            country_poly = self.client['world_data']['countries'].find_one({'properties.SU_A3' : key})
        if country_poly is None:
            print("Error retrieving %s polygon." % key)
            return None
        return country_poly['geometry']

    def get_all(self,collection,filter={},projection={'_id':0}):
        res = self.client['world_data'][collection].find(filter,projection)
        return self._make_result_list(res)
    

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

def haversine(point1, point2, miles=True):
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """

    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(math.radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = math.sin(lat * 0.5) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(lng * 0.5) ** 2
    # h = 2 * RADIUS_KM * math.asin(math.sqrt(d))
    h = 2 * math.asin(math.sqrt(d))
    
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers

def run_tests():
    """
    Ok, not really "tests" but mostly just exmaples....
    """
    mh = MongoHelper()

    print("Getting airports near within 200 miles of: (-98.5034180, 33.9382331)")
    res = mh.get_features_near_me('airports',(-98.5034180, 33.9382331),200)
    print("Found %d airports" % len(res))
    print("")

    print("Getting countries that have 'High income' in the INCOME_GRP field.")
    res = mh.get_doc_by_keyword('countries','properties.INCOME_GRP','High income')
    print("Found %d countries" % len(res))
    print("")

    print("Getting earthquakes that had a magnitude of 5.5 (not a partial match like above), and don't pass in 5.5 as a string!")
    res = mh.get_doc_by_keyword('earthquakes','properties.mag',5.5,False)
    print("Found %d earthquakes" % len(res))
    print("")

    print("Getting a state polygon.")
    state = mh.get_state_poly('co')
    print("Found %d polygon in the result." % len(state['coordinates']))
    print("")

    print("Getting all airports within the state poly from the previous query.")
    res = mh.get_feature_in_poly('airports',state['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")
   
    # Getting polygon data for Belgium
    country = mh.get_country_poly('BEL')

    # This query chokes on countries with type: MultiPolygon, but works on Polygon. 
    # I'm investigating ... (If we think about it, we probaly just need run one 
    # query per polygon within the "multi" polygon. 
    print("Getting all airports within the country poly from the previous query.")
    res = mh.get_feature_in_poly('airports',country['coordinates'])
    print("Found %d airports in the polygon." % len(res))
    print("")

    print("Getting the country that encompasses the point [44.2968750,24.6669864]")
    res = mh.get_poly_by_point('countries',[44.2968750,24.6669864])
    print("That country is: %s" % (res['properties']['NAME_LONG']))

    res = mh.get_all('airports')
    print(len(res))

if __name__=='__main__':
    mh = MongoHelper()
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    background_colour = (255,255,255)
    red = (255, 0, 0)
    green = (0,255,0)
    (width, height) = (1024, 512)
    color_list = {'airports': (0,0,255),'volcanos':(255,0,0),'earthquakes':(255,255,0),'meteorites':(165,42,42)}

    screen = pygame.display.set_mode((width, height))

    screen.fill(background_colour)

    bg = pygame.image.load(DIRPATH +'/draw_world_map/images/1024x512.png') 
    azurePin = pygame.image.load(DIRPATH +'/draw_world_map/images/icons/map_pins/PNG/Centered/16x16/MapMarker_Ball__Azure.png')
    pinkPin = pygame.image.load(DIRPATH +'/draw_world_map/images/icons/map_pins/PNG/Centered/16x16/MapMarker_Ball__Pink.png')
    
    points = []
    extremes = {}

    ap_list = []
    apPath_list = []
    final = []
    feature_list = ['volcanos', 'earthquakes', 'meteorites']
    adj = {'volcanoes': None, 'earthquakes': None, 'meteorites': None}
    searchRad = 500
    shortestDistance = 999999
    closest = None
    debug = 1

    running = True
    firstClick = False
    secondClick = False
    finished = False

    converted = False
    
    if len(sys.argv) > 1:
        firstClick = True
        secondClick = True
        startPoint = sys.argv[1]
        endPoint = sys.argv[2]
        searchRad = float(sys.argv[3])
        

        start =  mh.get_doc_by_keyword('airports','properties.ap_iata',startPoint)
        startPoint = (start[0]['geometry']['coordinates'][1],start[0]['geometry']['coordinates'][0])
        pt_list.append(start_coords)

        end =  mh.get_doc_by_keyword('airports','properties.ap_iata',endPoint)
        endPoint = (end[0]['geometry']['coordinates'][1],end[0]['geometry']['coordinates'][0])
        
    
    screen.blit(bg, (0, 0))
    pygame.display.flip()

    while running:
        pygame.event.pump()
        event = pygame.event.wait()
        mouse = pygame.mouse.get_pressed()

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and mouse[0] == True and firstClick == False:
            startPoint = (mapH.y_to_lat(event.pos[1],height),mapH.x_to_lon(event.pos[0],width))
            screen.blit(azurePin, event.pos)
            pygame.display.flip()
            firstClick = True
        if event.type == pygame.MOUSEBUTTONDOWN and mouse[2] == True and secondClick == False:
            endPoint = (mapH.y_to_lat(event.pos[1],height), mapH.x_to_lon(event.pos[0],width))
            screen.blit(pinkPin, event.pos)
            pygame.display.flip()
            secondClick = True
            
        if firstClick == True and secondClick == True and finished == False:
            while finished == False:
                ap_list = mh.get_features_near_me('airports', (startPoint[1], startPoint[0]), int(searchRad))

                for ap in ap_list:
                    x = ap['geometry']['coordinates'][0]
                    y = ap['geometry']['coordinates'][1]
                    distance = haversine((x,y),endPoint)
                    if distance < shortestDistance:
                        closest = (x,y)
                        shortestDistance = distance
                apPath_list.append(closest)
                startPoint = closest
                if haversine(startPoint, endPoint) < searchRad:
                    finished = True
        
        if converted == False and finished == True:
            apPath_list.append(endPoint)
            for ap in apPath_list:
                x = mapH.mercX(ap[0])
                y = mapH.mercY(ap[1])
                final.append((x,y))
            airports = mapH.adjust_location_coords(extremes,final,width,height)
            converted = True

        if converted == True and finished == True:
            for ap in apPath_list:
                for f in feature_list:
                    result_list = mh.get_features_near_me(f,(ap[1], ap[0]), searchRad)
                    extremes,points = mapH.find_extremes(result_list, width, height)
                    adj[f] = (mapH.adjust_location_coords(extremes,points,width,height))
                    for pt in adj[f]:
                        pygame.draw.circle(screen, color_list[f], pt, 2, 1)
                        pygame.dispay.flip()
            pygame.draw.lines(screen, green, False, airports)
            
        
                 


    