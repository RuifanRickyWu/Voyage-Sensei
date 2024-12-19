from intelligence.llm_agent import LLMAgent
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference


class UserIntentClient:
    _llm_agent: LLMAgent

    #this should be a classification task, this ask for rec should be replaced by another class
    _ask_for_recommendation: AskForRecommendation
    _provide_preference: ProvidePreference
    _system_response: str

    def __init__(self, llm_agent: LLMAgent, ask_for_recommendation: AskForRecommendation, provide_reference: ProvidePreference):
        self._llm_agent = llm_agent
        self._ask_for_recommendation = ask_for_recommendation
        self._provide_preference = provide_reference
        self._system_response = None
    
    def check_for_recommendation(self, query):
        template = self._ask_for_recommendation.get_prompt_for_classification(query)
        result = self._llm_agent.make_request(template)
        if result == "True":
            return True
        else:
            return False

#todo: finish this with only ask for recommendation intent
#todo: update classification for different intent

    def check_provide_preference(self, query):
        template = self._provide_preference.get_prompt_for_classification(query)
        result = self._llm_agent.make_request(template)
        if_provide_preference = result.split('\n')[0]
        if if_provide_preference == "True":
            self._system_response = result.split('\n')[1]
            return True
        else:
            return False
        
    def get_system_response(self):
        return self._system_response