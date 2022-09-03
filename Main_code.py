import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
import matplotlib
matplotlib.use('QtAgg')
from Parcel_Properties import Properties
from pandasql import sqldf
from defs import genrate_new_points_square_grid


mysql = lambda q: sqldf(q, globals())


def simplify_polygons(polygon,trehold,distanse):      
    # Doglas poker to reduse point numbers
    simplify=gpd.GeoDataFrame(geometry=[polygon.simplify(trehold, preserve_topology=False)])
    points_all=list(simplify.geometry[0].exterior.coords)
    
    # moving vertcies and create new points from it   
    new_points=genrate_new_points_square_grid(points_all,distanse)
    
    # closeing polygon from new points
    new_points[0]=new_points[-1]
    
    # list to polygon
    simple_polygon = Polygon([[p[0], p[1]] for p in new_points]) 
    simple_polygon = gpd.GeoDataFrame(geometry=[simple_polygon])
    return simple_polygon


def submit(shapfile_address,save_address,Doglas_poker_t,list_of_dist,area_limit):
   parcels = gpd.GeoDataFrame(geometry=[])
   lands=gpd.read_file(shapfile_address,encoding='utf-8')
   for i in range(len(lands)):
       polygon=Polygon(lands.geometry[i])
       simple_polygon=process(polygon,Doglas_poker_t,list_of_dist,area_limit)
       parcels = gpd.GeoDataFrame( pd.concat( [parcels,simple_polygon]))
   parcels.to_file(save_address)




def submit_i(i,shapfile_address,save_address,Doglas_poker_t,list_of_dist,area_limit):
   lands=gpd.read_file(shapfile_address,encoding='utf-8')
   polygon=Polygon(lands.geometry[i])
   simple_polygon=simple_polygon=process(polygon,Doglas_poker_t,list_of_dist,area_limit)
   simple_polygon.to_file(save_address)
   
def process(polygon,Doglas_poker_t,list_of_dist,area_limit):
    land = gpd.GeoDataFrame(geometry=[polygon])
    properties= Properties(land)
    if Doglas_poker_t=='':
        trehold=properties['EdgeShort']
    else: 
        trehold=float(Doglas_poker_t)
    if list_of_dist=='':
        t=properties['EdgeShort']
        distanse=[t/4,t/3,t/2,t,3*t/2]
    else: 
        distanse=[float(s) for s in list_of_dist.split(',')]
    if area_limit=='':
        area_limit=0
    else :
       area_limit=float(area_limit)
    s=float(properties['Area'])

    if s>area_limit:
        simple_polygon=simplify_polygons(polygon,trehold,distanse)
        simple_polygon['process']=1
    else:
        simple_polygon=land
        simple_polygon['process']=0
    return  simple_polygon
    

