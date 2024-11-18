from intelligence.wrapper.llm_wrapper import LLMWrapper


class LLMClient:
    _agent: LLMWrapper

    def __init__(self, llm_wrapper: LLMWrapper):
        self._agent = llm_wrapper

    def make_request(self, message):
        return self._agent.make_request(message)
