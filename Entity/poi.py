import numpy as np
import json
import geopandas as gpd
from io import StringIO

class POI:
    _id: str
    _address: str
    _name: str
    _description: str
    _feature: list[str]
    _embedding_metrix: np.ndarray
    _geo_info: gpd.GeoDataFrame
    def __init__(self, id:str, name:str, description:str, feature:list[str], embedding_metrix:np.ndarray, geo_info:json = None):
        self._id = id
        self._name = name
        self._description = description
        self._feature = feature
        self._geo_info = gpd.read_file(StringIO(geo_info)) if geo_info is not None else None
        self._embedding_metrix = embedding_metrix


    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_feature(self):
        return self._feature

    def get_embedding_metrix(self):
        return self._embedding_metrix

    def get_geo_info(self):
        return self._geo_info


