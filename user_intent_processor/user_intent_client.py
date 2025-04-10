from intelligence.llm_agent import LLMAgent
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference
from user_intent_processor.user_intent.cut_off_input import CutOffInput


class UserIntentClient:
    _llm_agent: LLMAgent

    #this should be a classification task, this ask for rec should be replaced by another class
    _ask_for_recommendation: AskForRecommendation
    _provide_preference: ProvidePreference
    _system_response: str

    def __init__(self, llm_agent: LLMAgent, ask_for_recommendation: AskForRecommendation, provide_reference: ProvidePreference, cut_off_input: CutOffInput):
        self._llm_agent = llm_agent
        self._ask_for_recommendation = ask_for_recommendation
        self._provide_preference = provide_reference
        self._cut_off_input = cut_off_input
        self._system_response = None
        self._remaining_mi = None
    
    def check_for_recommendation(self, query):
        template = self._ask_for_recommendation.get_prompt_for_classification(query)
        result = self._llm_agent.make_request(template)
        if result == "True":
            return True
        else:
            return False

#todo: finish this with only ask for recommendation intent
#todo: update classification for different intent

    def check_provide_preference(self, query, last_system_response, remaining_mandatory_information):
        template = self._provide_preference.get_prompt_for_classification(query, last_system_response, remaining_mandatory_information)
        result = self._llm_agent.make_request(template)
        if_provide_preference = result.split('\n')[0]
        if if_provide_preference == "True":
            self._system_response = result.split('\n')[1]
            self._remaining_mi = result.split("\n")[2]
            return True
        else:
            self._system_response = result.split('\n')[1]
            self._remaining_mi = result.split("\n")[2]
            if self._remaining_mi == "None": # time for recommendation
                print("ask for rec + no remaining_MI")
                return False
            else:
                print("still remaining_MI")
                print(self._remaining_mi)
                return True
    
    # note: utilized old 'ask for rec' prompt, but it's actually just provide preference but removed mandatory information check just for critiquing
    def check_provide_preference_critiquing(self, query, last_system_response):
        template = self._ask_for_recommendation.get_prompt_for_classification(query, last_system_response)
        result = self._llm_agent.make_request(template)
        if_provide_preference = result.split('\n')[0]
        if if_provide_preference == "True":
            self._system_response = result.split('\n')[1]
            return True
        else:
            self._system_response = result.split('\n')[1]
            print("ask for rec")
            return False
        
    def check_cut_off_input(self, query):
        template = self._cut_off_input.get_prompt_for_classification(query)
        result = self._llm_agent.make_request(template)
        if_cut_off_input = result.split('\n')[0]
        if if_cut_off_input == "True":
            self._system_response = result.split('\n')[1]
            return True
        else:
            return False
        
    def get_system_response(self):
        return self._system_response