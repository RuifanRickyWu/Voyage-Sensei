from intelligence.llm_agent import LLMAgent
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation


class UserIntentClient:
    _llm_agent: LLMAgent

    #this should be a classification task, this ask for rec should be replaced by another class
    _ask_for_recommendation: AskForRecommendation

    def __init__(self, llm_agent: LLMAgent, ask_for_recommendation: AskForRecommendation):
        self._llm_agent = llm_agent
        self._ask_for_recommendation = ask_for_recommendation

    def check_for_recommendation(self, query):
        template = self._ask_for_recommendation.get_prompt_for_classification(query)
        result = self._llm_agent.make_request(template)
        if result == "True":
            return True
        else:
            return False

#todo: finish this with only ask for recommendation intent
#todo: update classification for different intent
