from information_retriever.information_retrival_service import InformationRetrivalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService
from geo_processor.geo_service import GeoService


class QueryService:
    _ir_service: InformationRetrivalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService
    _geo_service: GeoService

    def __init__(self, ir_service: InformationRetrivalService,
                       user_intent_service: UserIntentService,
                       planning_service: PlanningService,
                       geo_service: GeoService):
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service
        self._geo_service = geo_service

    def append_query_or_recommend(self, query: str, state_manager: StateManager):
        recommendation_check = self._user_intent_service.check_for_recommendation(query)
        if recommendation_check == "False":
            state_manager.update_query(query)
            print(state_manager.get_query())
        else:
            state_manager.update_query(query)
            print(state_manager.get_query())
            search_result = self._ir_service.get_topk_poi_llm_search(state_manager, 5)
            poi_sequence= self._planning_service.plan_with_llm_planner(state_manager, search_result)
            print(poi_sequence)
            return poi_sequence

        return "query_updated"

    def get_current_plan(self, state_manager: StateManager):
        if state_manager.get_current_plan() is None:
            return "No plans created yet"
        else:
            return self._geo_service.get_coords_from_plan(state_manager)
