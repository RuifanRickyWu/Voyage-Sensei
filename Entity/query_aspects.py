from .aspect import *
from .query import *
import json

class QueryAspects:
    """
    A class that serves as an organized layer for capturing all aspects from json output.
    Flattens all constraints and preferences.
    NOTE: Class Abandoned
    """
    def __init__(self, query: str, json_path: str):
        self.query = query
        self.json_path = json_path
        
        # objective constraints
        self.type_poi = None
        self.location = None
        self.features_hard = []
        self.distance = []
        self.price = []
        
        # soft aspects
        self.features_soft = []
        self.emotions_important = []
        self.emotions_less_important = []
        self.inferenced_aspects = []
        
        
    def load(self): 
        with open(self.json_path, 'r') as file:
            data = json.load(file)
            print("\ndata: ")
            print(data)