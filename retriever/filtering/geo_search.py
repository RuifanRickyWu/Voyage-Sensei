import osmnx as ox
import geopandas as gpd
import os
import json
from CarTravel.Entity.poi import POI

class GeoSearch():
    
    def __init__(self):
        pass
        
        
    def get_pois_within_distance(self, distance: float, starting_location, pois: list[POI]):
        
        # print(os.environ['OSMNX_CACHE_DIR'])
        # os.environ['OSMNX_CACHE_DIR'] = 'CarTravel/geo_cache'
        gdf_start = ox.geocode_to_gdf(starting_location)

        selected = []
        for poi in pois:
            if poi.get_geo_info() is not None:
                d = self._get_distance(gdf_start, poi.get_geo_info())
                #print(f"Distance: {d} km")
                if d <= distance:
                    #print("Selected:")
                    #print(poi.get_name())
                    selected.append(poi)
                if d > 10000:
                    print(poi.get_name())
        return selected
    
    def _get_distance(self, gdf_start, gdf):
        
        g1 = gdf_start.to_crs(crs=3857)
        g2 = gdf.to_crs(crs=3857)
        
        d = g1.distance(g2.iloc[0].geometry) / 1000
        return d.iloc[0].round(2)