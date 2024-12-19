from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference
from user_intent_processor.user_intent_client import UserIntentClient
from state.state_manager import StateManager

class UserIntentService:
    _prompt_config: dict
    _ask_for_recommendation: AskForRecommendation
    _user_intent_client: UserIntentClient
    _state_manager: StateManager

    def __init__(self, user_intent_client: UserIntentClient, ask_for_recommendation: AskForRecommendation, state_manager: StateManager):
        self._ask_for_recommendation = ask_for_recommendation
        self._user_intent_client = user_intent_client
        self._state_manager = state_manager

    def check_for_recommendation(self, query: str):
        return self._user_intent_client.check_for_recommendation(query)

    def check_provide_preference(self, query: str):
        return self._user_intent_client.check_provide_preference(query)
    
    def append_system_response(self):
        system_response = self._user_intent_client.get_system_response()
        self._state_manager.append_system_response(system_response)