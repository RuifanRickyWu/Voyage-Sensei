from state.state_entity.POI import POI


class SessionHistory:
    _user_queries: list[str]
    _user_query_aspects: list[str]
    _system_responses: list[str]
    _user_critiques: list[str]

    def __init__(self):
        self._user_queries = []
        self._user_query_aspects = []
        self._user_critiques = []
        self._system_responses = []

    def append_queries(self, query: str):
        self._user_queries.append(query)

    def append_critiques(self, critiques: str):
        self._user_critiques.append(critiques)

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
        print(self._system_responses)
    
    def get_lastest_system_response(self):
        return self._system_responses[-1]