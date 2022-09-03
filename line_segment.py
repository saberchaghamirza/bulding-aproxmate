# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 14:07:30 2022

@author: saber
"""
from shapely.geometry import Polygon,LineString
import geopandas as gpd


def line_segment(single_geodataframe):
    line_segs = gpd.GeoSeries(
    single_geodataframe["geometry"]
    .apply(
        lambda g: [g]
        if isinstance(g,Polygon)
        else [p for p in g.geoms]
    )
    .apply(
        lambda l: [
            LineString([c1, c2])
            for p in l
            for c1, c2 in zip(p.exterior.coords, list(p.exterior.coords)[1:])
        ]
    )
    .explode()
    )
    return line_segs