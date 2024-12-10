from state.state_entity.POI import POI


class SessionHistory:
    _user_queries: list[str]
    _user_query_aspects: list[str]
    _current_search_list: list[POI]

    def __init__(self):
        self._user_queries = []
        self._current_search_list = []
        self._user_query_aspects = []

    def append_queries(self, query: str):
        self._user_queries.append(query)

    def get_queries(self):
        return self._user_queries

    def update_current_search_list(self, poi_list=list[POI]):
        self._current_search_list = poi_list

    def get_current_search_list(self):
        return self._current_search_list

    #tbd: replace with a new list or just append new aspects
    #also need to do conversion for the input format
    def update_query_aspects(self, query_aspects: list[str]):
        self._user_query_aspects.append(query_aspects)

    def get_query_aspects(self):
        return self._user_query_aspects