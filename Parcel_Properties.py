import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon,Point
import pandas as pd
from pandasql import sqldf
from line_segment import line_segment
#... گرفتن اطلاعات لازم در جدول بالایی فرم جهاد 

# get the utm points
# get the utm points
def Properties(land):
    global boundsxy
    global all_points
    global rowdata
    global data
    global new_data
    global lines

    center=land.centroid
    x_center=center.x
    y_center=center.y
    points_all=list(land.geometry[0].exterior.coords)
    all_points=pd.DataFrame(points_all,columns=['x','y'])
    all_points['d_center']=np.sqrt((all_points['x']-x_center)**2+(all_points['y']-y_center)**2)

    mysql = lambda q: sqldf(q, globals()) 
################################ 
# lowst and longst edge
    polygon=Polygon(land.geometry[0])   
    land = gpd.GeoDataFrame(geometry=[polygon])
    all_line=line_segment(land)
    lines=pd.DataFrame(all_line.length,columns=['lenght'])
    
    query='''
    SELECT max(lenght) long, min(lenght) short
    from  lines ;
    '''
    edges=mysql(query)  
    edge_long=float(edges.long)
    edge_short=float(edges.short)
    len_of_lines=len(lines)
###################################################################
# longest Diameter
    query='''
    SELECT max(d_center) dist1,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''
    point1=mysql(query)
    p1=Point(point1.x,point1.y)
    # get secend point 
    all_points['distance']=np.sqrt((all_points['x']-p1.x)**2+(all_points['y']-p1.y)**2)

    query='''
    SELECT max(p.distance) dist,ROUND(p.x,2) x,ROUND(p.y,2) y
    from
      (select distance from all_points
       EXCEPT
      select lenght from lines) e, all_points p
      where p.distance=e.distance
    '''
    point2=mysql(query)
    
    LONG_lenght=float(point2.dist)
########################################################################
# lowest Diameter
    query='''
    SELECT min(d_center) dist1,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''
    
    point1_min=mysql(query)
    p1_min=Point(point1_min.x,point1_min.y)
    # get secend point 
    all_points['d_p1_min']=np.sqrt((all_points['x']-p1_min.x)**2+(all_points['y']-p1_min.y)**2)
    query='''
            SELECT min(p.distance) dist,ROUND(p.x,2) x,ROUND(p.y,2) y
            from
              (select distance from all_points
               EXCEPT
              select lenght from lines) e, all_points p
              where p.distance=e.distance
      ''' 
    point2_min=mysql(query)

    Short_lenght=float(point2_min.dist)
#######################################
    area=float(land.area)
    area_convex_hull=float(land.convex_hull.area)
    area_envelope=float(land.envelope.area)
    border_points =({'Area':area,'convex_hull':area_convex_hull,'envelope':area_envelope,'EdgeNumber':len_of_lines,'EdgeLong':edge_long,'EdgeShort':edge_short,'LongDiameterLenght':LONG_lenght,'ShortDiameterLenght':Short_lenght})
    return border_points


