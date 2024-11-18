from intelligence.wrapper.llm_wrapper import LLMWrapper
from intelligence.llm_client import LLMClient
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation


class UserIntentService:
    _llm_client: LLMClient
    _prompt_config: dict
    _ask_for_recommendation: AskForRecommendation

    def __init__(self, llm_client: LLMClient, ask_for_recommendation: AskForRecommendation):
        self._llm_client = llm_client
        self._ask_for_recommendation = ask_for_recommendation

    def check_for_recommendation(self, query):
        template = self._ask_for_recommendation.get_prompt_for_classification(query)
        return self._llm_client.make_request(template)
