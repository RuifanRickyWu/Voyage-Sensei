from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference
from user_intent_processor.user_intent_client import UserIntentClient
from state.state_manager import StateManager

class UserIntentService:
    _prompt_config: dict
    _ask_for_recommendation: AskForRecommendation
    _user_intent_client: UserIntentClient

    def __init__(self, user_intent_client: UserIntentClient, ask_for_recommendation: AskForRecommendation):
        self._ask_for_recommendation = ask_for_recommendation
        self._user_intent_client = user_intent_client

    def check_for_recommendation(self, query: str):
        return self._user_intent_client.check_for_recommendation(query)

    def check_provide_preference(self, query: str):
        return self._user_intent_client.check_provide_preference(query)
    
    def append_system_response(self, state_manager: StateManager):
        system_response = self._user_intent_client.get_system_response()
        state_manager.append_system_response(system_response)
