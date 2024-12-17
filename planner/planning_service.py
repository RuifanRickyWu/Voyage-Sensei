from planner.planning_client.llm_planning_client import LLMPlanningClient
from state.state_manager import StateManager


class PlanningService:
    _llm_planning_client: LLMPlanningClient

    def __init__(self, llm_planning_client: LLMPlanningClient):
        self._llm_planning_client = llm_planning_client

    def llm_planning(self, state_manager: StateManager):
        queries = state_manager.get_query()
        poi_list = state_manager.get_current_search_result().get_converted_retrieved_poi_list()
        self._llm_planning_client.llm_planning(state_manager, queries, poi_list)


