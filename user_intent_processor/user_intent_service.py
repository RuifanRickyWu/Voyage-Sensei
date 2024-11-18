from intelligence.wrapper.llm_wrapper import LLMWrapper
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation


class UserIntentService:
    _agent: LLMWrapper
    _prompt_config: dict
    _ask_for_recommendation: AskForRecommendation

    def __init__(self, agent: LLMWrapper, ask_for_recommendation: AskForRecommendation):
        self._agent = agent
        self._ask_for_recommendation = ask_for_recommendation

    def check_for_recommendation(self, query):
        template = self._ask_for_recommendation.get_prompt_for_classification(query)
        return self._agent.make_request(template)
