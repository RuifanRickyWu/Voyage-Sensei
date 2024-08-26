from .aspect import *

class Query:
    """
    A class represents a user's travel destinations query.
    A query contains a list of preferences and constraints.
    """
    def __init__(self, description: str):
        self.description = description
        self.aspects = []

    def get_all_aspects(self) -> list[Aspect]:
        return self.aspects
        
    def get_description(self) -> str:
        return self.description # return the query
        
    def get_navigational_constraints(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Objective_Constraint)]
        
    def get_range_constraints(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Range_Constraint)]
    
    def get_navigational_preference(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Objective_Preference)]

    def get_dir_subjective_constraints(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Direct_Subjective_Constraints)]
    
    def get_dir_subjective_preferences(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Direct_Subjective_Preference)]
    
    def get_indirect_aspects(self):
        return [aspect for aspect in self.aspects if isinstance(aspect, Indirect_Aspect)]
    
    def add_aspect(self, aspect: Aspect):
        self.aspects.append(aspect)