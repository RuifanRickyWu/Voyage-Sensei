import logging
from information_retriever.information_retrieval_service import InformationRetrievalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from reasoner.reasoning_service import ReasoningService
from event_processor.event_processor_service import EventProcessorService

class CritiqueService:

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


    def append_critique_or_recommend(self, critique: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(critique)

        if recommendation_check:
            self.logger.info("Start Critique Recommendation")
            state_manager.update_critique(critique)
            self.logger.info(f"Current Critique List -> : {state_manager.get_critique()}")




        state_manager.update_critique(critique)
        self.logger.info(f"Current Query List -> : {state_manager.get_critique()}")