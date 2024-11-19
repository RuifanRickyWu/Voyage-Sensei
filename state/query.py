class Query:
    """
    A class represents a user's travel destinations query.
    A query contains a list of preferences and constraints.
    """
    def __init__(self, description: str):
        self.description = description
        self.aspects = None
        # self.ask_for_recommendation = False
        
    def set_aspects(self, aspects: str):
        '''
        aspects are stored in a query object as a string with JSON
        '''
        self.aspects = aspects
        
    # def ask_for_recommendation(self):
    #     self.ask_for_recommendation = True