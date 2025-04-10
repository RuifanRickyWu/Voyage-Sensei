import logging

from information_retriever.information_retrieval_service import InformationRetrievalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from reasoner.reasoning_service import ReasoningService
from event_processor.event_processor_service import EventProcessorService


class QueryService:
    _ir_service: InformationRetrievalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService
    _geo_service: GeoService
    _reasoning_service: ReasoningService
    _event_processor_service: EventProcessorService

    def __init__(self, ir_service: InformationRetrievalService,
                       user_intent_service: UserIntentService,
                       planning_service: PlanningService,
                       geo_service: GeoService,
                       query_processing_service: QueryProcessingService,
                       reasoning_service: ReasoningService,
                       event_processor_service: EventProcessorService):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self._geo_service = geo_service
        self.query_processing_service = query_processing_service
        self._reasoning_service = reasoning_service
        self._event_processor_service = event_processor_service

    # MVP: pass all user queries
    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        
        cut_off_check = self._user_intent_service.check_cut_off_input(query)
        
        if cut_off_check:
            self._user_intent_service.append_system_response(state_manager)
            return state_manager.get_latest_system_response()
                
        # recommendation_check = self._user_intent_service.check_for_recommendation(query)
        
        last_system_response = state_manager.get_latest_system_response()
        remaining_mandatory_information = state_manager.get_remaining_mandatory_information()
        provide_preference_check = self._user_intent_service.check_provide_preference(query, last_system_response, remaining_mandatory_information)
        
        print("--------------------")
        print(provide_preference_check)
        print(remaining_mandatory_information)

        if not provide_preference_check and remaining_mandatory_information == "None":
            self.logger.info("Start Recommendation")
            state_manager.update_query(query)
            self.logger.info(f"Current Query List -> : {state_manager.get_query()}")
            self._ir_service.llm_search_get_top_k(state_manager, 2)
            self._event_processor_service.search_for_event(state_manager)
            self._planning_service.llm_planning(state_manager)
            self._geo_service.get_coords_for_plan(state_manager)
            self._reasoning_service.reason_for_trip(state_manager)
            #one time thing
            state_manager.update_init_trip()
            return state_manager.get_current_plan().form_current_plan()

        state_manager.update_query(query)
        self.logger.info(f"Current Query List -> : {state_manager.get_query()}")
        # append system response
        self._user_intent_service.append_system_response(state_manager)
        self._user_intent_service.update_remaining_mi(state_manager)
        
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

    def form_init_trip(self, state_manager: StateManager):
        if state_manager.get_init_trip().get_poi_in_sequence() is None:
            return "No initial Trip created yet"
        return state_manager.get_init_trip().form_current_plan_full_detail()



