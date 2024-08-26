from abc import ABC

class Aspect(ABC):
    """
    An base class representing an aspect of a user query, characterized by a description.

    :param description (str): A textual description of the aspect.
    """
    def __init__(self, description: str):
        self.description = description
        # self.new_description = description 
    
    # def set_new_description(self, new_description: str):
    #     self.new_description = new_description
    
    def get_original_description(self) -> str:
        return self.description

class Objective_Constraint(Aspect):
    def __init__(self, description: str):
        super().__init__(description)

class Range_Constraint(Aspect):
    def __init__(self, description: str):
        super().__init__(description)
        self.value = (0, 1000)
        
class Objective_Preference(Aspect):  
    def __init__(self, description: str):
        super().__init__(description)
        
class Direct_Subjective_Constraints(Aspect):
    def __init__(self, description: str):
        super().__init__(description)

class Direct_Subjective_Preference(Aspect):
    def __init__(self, description: str):
        super().__init__(description)

class Indirect_Aspect(Aspect):
    def __init__(self, description: str, goals: list[str]):
        super().__init__(description)
        self.goals = goals
        
    def get_goals(self) -> str:
        return self.goals