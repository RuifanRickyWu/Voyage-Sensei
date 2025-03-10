from state.state_entity.current_plan import CurrentPlan
from state.state_entity.current_search import CurrentSearch
from state.state_entity.session_history import SessionHistory


class StateManager:
    _session_history: SessionHistory
    _current_search: CurrentSearch
    _current_plan: CurrentPlan

    def __init__(self):
        self._session_history = SessionHistory()
        self._current_search = CurrentSearch()
        self._current_plan = CurrentPlan()

    def get_query(self):
        return self._session_history.get_queries()

    def update_query(self, new_query : str):
        self._session_history.append_queries(new_query)
        
    def get_aspects(self):
        return self._session_history.get_query_aspects()
        
    def update_aspects(self, aspects : list[str]):
        self._session_history.update_query_aspects(aspects)

    def get_current_plan(self):
        return self._current_plan

    def update_current_plan(self, current_plan: CurrentPlan):
        self._current_plan = current_plan

    def get_current_search_result(self):
        return self._current_search

    def update_current_search_result(self, current_search: CurrentSearch):
        self._current_search = current_search
    
    # for responding to the user in the UI    
    # for providing last system response to the next iteration of conversation
    def get_latest_system_response(self):
        return self._session_history.get_lastest_system_response()
    
    # update and get remaining mandatory information
    def get_remaining_mandatory_information(self):
        return self._session_history.get_remaining_mandatory_information()
    
    def update_remaining_mandatory_information(self, remaining_mi):
        self._session_history.update_remaining_mandatory_information(remaining_mi)
    
    def append_system_response(self, system_response):
        self._session_history.append_system_response(system_response)
