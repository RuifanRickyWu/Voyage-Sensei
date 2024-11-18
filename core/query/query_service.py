from information_retriever.information_retrival_service import InformationRetrivalService
from state.state_manager import StateManager
from user_intent_processor.user_intent_service import UserIntentService
from planner.planning_service import PlanningService


class QueryService:
    _ir_service: InformationRetrivalService
    _planning_service: PlanningService
    _user_intent_service: UserIntentService

    def __init__(self, ir_service: InformationRetrivalService, user_intent_service: UserIntentService, planning_service: PlanningService):
        self._ir_service = ir_service
        self._user_intent_service = user_intent_service
        self._planning_service = planning_service

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
