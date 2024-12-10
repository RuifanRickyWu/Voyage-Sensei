from typing import Any
from state.state_entity.POI import POI
from state.state_entity.itinerary import Itinerary
from state.state_entity.session_history import SessionHistory


class StateManager:
    #temp
    _query: list[str]
    _current_plan: list[dict]

    _session_history: SessionHistory
    _itinerary: Itinerary

    def __init__(self):
        self._query = []
        self._aspects = []
        self._current_plan = None

        self._session_history = SessionHistory()
        self._itinerary = Itinerary()

    def get(self, key: str) -> Any:
        pass

    def update(self, key: str, value: Any):
        pass

    def get_query(self):
        return self._session_history.get_queries()

    def update_query(self, new_query : str):
        self._session_history.append_queries(new_query)
        
    def get_aspects(self):
        return self._aspects
        
    def update_aspects(self, aspects : list[str]):
        self._aspects = aspects

    def get_current_plan(self):
        return self._current_plan

    def update_current_plan(self, plan: list[dict]):
        self._current_plan = plan
