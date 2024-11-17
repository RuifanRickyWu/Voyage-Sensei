import json

from information_retriever.search_engine.llm_search_engine import LLMSearchEngine
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning.llm_planner import LLMPlanner


class QueryService:
    _llm_search_engine: LLMSearchEngine
    _user_intent_service: UserIntentService
    _llm_planner: LLMPlanner

    def __init__(self, llm_search_engine: LLMSearchEngine, user_intent_service: UserIntentService,llm_planner: LLMPlanner):
        self._llm_search_engine = llm_search_engine
        self._user_intent_service = user_intent_service
        self._llm_planner = llm_planner

    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        if recommendation_check == "False":
            state_manager.update_query(query)
            print(state_manager.get_query())
        else:
            state_manager.update_query(query)
            print(state_manager.get_query())
            search_result = json.loads(self._llm_search_engine.get_topk_poi(state_manager.get_query(), 5))
            print(search_result)
            poi_sequence = self._llm_planner.plan(state_manager.get_query(), search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"
