from state.state_entity.POI import POI


class SessionHistory:
    _user_queries: list[str]
    _user_query_aspects: list[str]
    _system_responses: list[str]

    def __init__(self):
        self._user_queries = []
        self._user_query_aspects = []
        self._system_responses = ['How Would You Like to Embark on Your Trip Today?']
        self._remaining_mandatory_information = "Time, Budget, Purpose"

    def append_queries(self, query: str):
        self._user_queries.append(query)

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
    
    # update and get remaining mandatory information
    def update_remaining_mandatory_information(self, remaining_mi):
        self._remaining_mandatory_information = remaining_mi
    
    def get_remaining_mandatory_information(self):
        return self._remaining_mandatory_information