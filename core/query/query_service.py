from information_retriever.information_retrieval_service import InformationRetrievalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from reasoner.reasoning_service import ReasoningService


class QueryService:
    _ir_service: InformationRetrievalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService
    _geo_service: GeoService
    _reasoning_service: ReasoningService

    def __init__(self, ir_service: InformationRetrievalService,
                       user_intent_service: UserIntentService,
                       planning_service: PlanningService,
                       geo_service: GeoService,
                       query_processing_service: QueryProcessingService,
                       reasoning_service: ReasoningService):
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self._geo_service = geo_service
        self.query_processing_service = query_processing_service
        self._reasoning_service = reasoning_service

    # MVP: pass all user queries
    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        provide_preference_check = self._user_intent_service.check_provide_preference(query)
        
        if provide_preference_check:
            state_manager.update_query(query)
            print(state_manager.get_query())
            
            # append system response
            self._user_intent_service.append_system_response(state_manager)
            return state_manager.get_latest_system_response()
        
        if recommendation_check:
            state_manager.update_query(query)
            print(state_manager.get_query())
            self._ir_service.llm_search_get_top_k(state_manager, 5)
            self._planning_service.llm_planning(state_manager)
            self._geo_service.get_coords_for_plan(state_manager)
            self._reasoning_service.reason_for_trip(state_manager)

            return state_manager.get_current_plan().form_current_plan()
        return state_manager.get_latest_system_response()

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
            
            search_result = self._ir_service.llm_search_get_top_k(state_manager.get_aspects(), 5)
            print(search_result)
            poi_sequence = self._planning_service.plan_with_llm_planner(state_manager.get_query(), search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"


    def form_full_plan(self, state_manager: StateManager):
        if state_manager.get_current_plan().get_poi_in_sequence() is None:
            return "No plans created yet"
        return state_manager.get_current_plan().form_current_plan_full_detail()



