from intelligence.wrapper.gpt_wrapper import GPTWrapper
from intelligence.wrapper.llm_wrapper import LLMWrapper


class LLMAgent:
    _agent: LLMWrapper

    def __init__(self, config:dict ,agent_type: str):
        if agent_type == "GPT":
            self._agent = GPTWrapper(config.get("OPENAI_API_KEY"))

    def make_request(self, message):
        return self._agent.make_request(message)
