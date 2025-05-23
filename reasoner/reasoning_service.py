from reasoner.reasoning_client import ReasoningClient
from state.state_manager import StateManager


class ReasoningService:

    _reasoning_client: ReasoningClient

    def __init__(self, reasoning_client: ReasoningClient):
        self._reasoning_client = reasoning_client

    def reason_for_trip(self,state_manager: StateManager):
        self._generate_keywords_for_poi(state_manager)
        self._generate_trip_summary(state_manager)

    def reason_for_trip_after_critique(self, state_manager: StateManager):
        self._generate_keywords_after_critique_for_poi(state_manager)
        self._generate_trip_summary_after_critique(state_manager)

    def _generate_keywords_for_poi(self, state_manager: StateManager):
        poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        queries = state_manager.get_query()
        self._reasoning_client.keyword_summarization_for_poi(state_manager, poi_list, queries)

    def _generate_keywords_after_critique_for_poi(self, state_manager: StateManager):
        poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        queries = state_manager.get_query()
        critiques = state_manager.get_critique()
        self._reasoning_client.keyword_summarization_after_critique_for_poi(state_manager, poi_list, queries, critiques)

    def _generate_trip_summary(self, state_manager: StateManager):
        poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        queries = state_manager.get_query()
        self._reasoning_client.trip_summary(state_manager, queries, poi_list)

    def _generate_trip_summary_after_critique(self, state_manager: StateManager):
        poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        queries = state_manager.get_query()
        critiques = state_manager.get_critique()
        self._reasoning_client.trip_summary(state_manager, queries, poi_list)
