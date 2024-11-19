from information_retriever.information_retrival_service import InformationRetrivalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService


class QueryService:
    _ir_service: InformationRetrivalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService

    def __init__(self, ir_service: InformationRetrivalService, user_intent_service: UserIntentService, planning_service: PlanningService, query_processing_service: QueryProcessingService):
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self.query_processing_service = query_processing_service

    # MVP: pass all user queries
    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        if recommendation_check == "False":
            state_manager.update_query(query)
            print(state_manager.get_query())
        else:
            state_manager.update_query(query)
            print(state_manager.get_query())
            search_result = self._ir_service.get_topk_poi_llm_search(state_manager.get_query(), 5)
            print(search_result)
            poi_sequence = self._planning_service.plan_with_llm_planner(state_manager.get_query(), search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"

    # Q2E: list of aspects
    def append_query_or_recommend_q2e(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        state_manager.update_query(query)
        if recommendation_check == "False":
            processor = self.query_processing_service
            processor.load_query(query)
            print(state_manager.get_aspects())
        else:
            processor = self.query_processing_service
            processor.load_query(query)
            aspects = processor.extract_aspects(processor.query_list)
            state_manager.update_aspects(aspects)
            print(state_manager.get_aspects())
            
            search_result = self._ir_service.get_topk_poi_llm_search(state_manager.get_aspects(), 5)
            print(search_result)
            poi_sequence = self._planning_service.plan_with_llm_planner(state_manager.get_query(), search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"