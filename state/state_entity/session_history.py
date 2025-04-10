from state.state_entity.POI import POI
from state.state_entity.current_plan import CurrentPlan


class SessionHistory:
    _user_queries: list[str]
    _user_query_aspects: list[str]
    _system_responses: list[str]
    _user_critiques: list[str]
    _latest_system_response: str
    _has_init_trip: bool

    def __init__(self):
        self._user_queries = []
        self._user_query_aspects = []
        self._system_responses = ['How Would You Like to Embark on Your Trip Today?']
        self._remaining_mandatory_information = "Time, Budget, Purpose"
        self._user_critiques = []
        self._latest_system_response = self._system_responses[-1]
        self._init_trip = CurrentPlan()

    def append_queries(self, query: str):
        self._user_queries.append(query)

    def update_init_trip(self, trip: CurrentPlan):
        self._init_trip = trip

    def get_init_trip(self):
        return self._init_trip

    def append_critiques(self, critiques: str):
        self._user_critiques.append(critiques)

    def clean_critiques(self):
        self._user_critiques = []

    def get_critiques(self):
        return self._user_critiques

    def get_queries(self):
        return self._user_queries

    #tbd: replace with a new list or just append new aspects
    #also need to do conversion for the input format
    def update_query_aspects(self, query_aspects: list[str]):
        self._user_query_aspects.append(query_aspects)

    def get_query_aspects(self):
        return self._user_query_aspects
    
    def append_system_response(self, system_response):
        self._system_responses.append(system_response)
    
    def get_latest_system_response(self):
        self._latest_system_response = self._system_responses[-1]
        return self._latest_system_response

    def clean_latest_system_response(self):
        self._latest_system_response = ""
    
    # update and get remaining mandatory information
    def update_remaining_mandatory_information(self, remaining_mi):
        self._remaining_mandatory_information = remaining_mi
    
    def get_remaining_mandatory_information(self):
        return self._remaining_mandatory_information