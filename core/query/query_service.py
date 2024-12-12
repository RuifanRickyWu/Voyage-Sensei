from information_retriever.information_retrival_service import InformationRetrivalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService


class QueryService:
    _ir_service: InformationRetrivalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService
    _geo_service: GeoService

    def __init__(self, ir_service: InformationRetrivalService,
                       user_intent_service: UserIntentService,
                       planning_service: PlanningService,
                       geo_service: GeoService,
                       query_processing_service: QueryProcessingService):
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self._geo_service = geo_service
        self.query_processing_service = query_processing_service

    # MVP: pass all user queries
    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        if not recommendation_check:
            state_manager.update_query(query)
            print(state_manager.get_query())
        else:
            state_manager.update_query(query)
            print(state_manager.get_query())
            search_result = self._ir_service.get_topk_poi_llm_search(state_manager, 10)
            plan= self._planning_service.plan_with_llm_planner(state_manager, search_result)
            self._geo_service.get_coords_for_plan(state_manager)
            return state_manager.get_current_plan()

        return "query_updated"

    # Q2E: list of aspects
    def append_query_or_recommend_q2e(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        state_manager.update_query(query)
        if not recommendation_check:
            print("\nrecommendation_check is false")
            processor = self.query_processing_service
            processor.load_query(query)
            print("we are printing aspects, which should be nothing:")
            print(state_manager.get_aspects())
        else:
            print("\nrecommendation_check is true")
            processor = self.query_processing_service
            processor.load_query(query)
            aspects = processor.process_queries()
            state_manager.update_aspects(aspects)
            
            print("we are printing aspects, which should have something:")
            print(state_manager.get_aspects())
            
            print("query has been processed, will continue to IR to search top k pois")
            
            search_result = self._ir_service.get_topk_poi_llm_search(state_manager.get_aspects(), 5)
            print(search_result)
            poi_sequence = self._planning_service.plan_with_llm_planner(state_manager.get_query(), search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"
      
    def get_current_plan(self, state_manager: StateManager):
        if state_manager.get_current_plan() is None:
            return "No plans created yet"
        else:
            return state_manager.get_current_plan()
