from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference
from user_intent_processor.user_intent.cut_off_input import CutOffInput
from user_intent_processor.user_intent_client import UserIntentClient
from state.state_manager import StateManager

class UserIntentService:
    _prompt_config: dict
    _ask_for_recommendation: AskForRecommendation
    _user_intent_client: UserIntentClient

    def __init__(self, user_intent_client: UserIntentClient, ask_for_recommendation: AskForRecommendation):
        self._ask_for_recommendation = ask_for_recommendation
        self._user_intent_client = user_intent_client

    # def check_for_recommendation(self, query: str):
    #     return self._user_intent_client.check_for_recommendation(query)

    def check_provide_preference(self, query: str, last_system_response: str, remaining_mandatory_information: str):
        return self._user_intent_client.check_provide_preference(query, last_system_response, remaining_mandatory_information)
    
    def check_cut_off_input(self, query: str):
        return self._user_intent_client.check_cut_off_input(query)
    
    def append_system_response(self, state_manager: StateManager):
        system_response = self._user_intent_client.get_system_response()
        state_manager.append_system_response(system_response)
        
    def update_remaining_mi(self, state_manager: StateManager):
        remaining_mi = self._user_intent_client._remaining_mi
        state_manager.update_remaining_mandatory_information(remaining_mi)
