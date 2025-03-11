import logging
from information_retriever.information_retrieval_service import InformationRetrievalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from reasoner.reasoning_service import ReasoningService
from event_processor.event_processor_service import EventProcessorService
from core.critique.critique_client.critique_client import CritiqueClient

class CritiqueService:

    _ir_service: InformationRetrievalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService
    _geo_service: GeoService
    _reasoning_service: ReasoningService
    _event_processor_service: EventProcessorService
    _critique_client: CritiqueClient

    def __init__(self, ir_service: InformationRetrievalService,
                       user_intent_service: UserIntentService,
                       planning_service: PlanningService,
                       geo_service: GeoService,
                       query_processing_service: QueryProcessingService,
                       reasoning_service: ReasoningService,
                       event_processor_service: EventProcessorService,
                       critique_client: CritiqueClient):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self._geo_service = geo_service
        self.query_processing_service = query_processing_service
        self._reasoning_service = reasoning_service
        self._event_processor_service = event_processor_service
        self._critique_client = critique_client


    def append_critique_or_recommend(self, critique: str, state_manager: StateManager):

        if state_manager.get_current_plan().get_converted_planned_poi_list() == None:
            return "Missing Initial Recommendation"

        cut_off_check = self._user_intent_service.check_cut_off_input(critique)

        if cut_off_check:
            self._user_intent_service.append_system_response(state_manager)
            return state_manager.get_latest_system_response()

        recommendation_check = self._user_intent_service.check_for_recommendation(critique)

        if recommendation_check:
            self.logger.info("Finish Critiquing, generating new trip")
            state_manager.update_critique(critique)
            self.logger.info(f"Current Critique List -> : {state_manager.get_critique()}")
            self.identify_and_remove_critiqued_poi(state_manager)
            self._ir_service.llm_search_during_critique(state_manager)
            self._planning_service.llm_planning_after_critique(state_manager)
            self._geo_service.get_coords_for_plan(state_manager)
            self._reasoning_service.reason_for_trip_after_critique(state_manager)
            return state_manager.get_current_plan().form_current_plan()

        state_manager.update_critique(critique)
        self.logger.info(f"Current Critique List -> : {state_manager.get_critique()}")
        # append system response
        self._user_intent_service.append_system_response(state_manager)
        return state_manager.get_latest_system_response()

    def identify_and_remove_critiqued_poi(self, state_manager: StateManager):
        self._critique_client.identify_and_remove_critiqued_poi(state_manager)

