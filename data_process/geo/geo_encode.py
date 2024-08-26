import osmnx as ox
import geopandas as gpd
import os
import json


class GeoEncode:
    def __init__(self):
        pass

    def geo_encode(self, name:str, address: str):
        try:
            gdf = ox.geocode_to_gdf(address)
            return gdf.to_json()
        except:
            print(name)
            print("Failed to geocode the following addresses:", address)
            print()
            return None
