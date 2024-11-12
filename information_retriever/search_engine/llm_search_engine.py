from intelligence.wrapper.llm_wrapper import LLMWrapper


class LLMSearchEngine:
    _agent: LLMWrapper
    def __init__(self, agent: LLMWrapper):
        self._agent = agent

    #Get k poi from GPT
    def get_topk_poi(self):
        self._agent.make_request()

