from intelligence.wrapper.llm_wrapper import LLMWrapper
from intelligence.wrapper.gpt_wrapper import GPTWrapper


class SingletonLLMAgent:
    _instance = None
    _agent: LLMWrapper = None
    _config: dict

    def __new__(cls, config: dict):
        if cls._instance is None:
            cls._instance = super(cls).__new__()
            cls._instance._config = config
        return cls._instance

    def get_agent(self) -> LLMWrapper:
        if self._agent is None:
            self._create_agent()
        return self._agent

    def _create_agent(self, agent_type:str = "gpt"):
        if agent_type == "gpt":
            self._agent = GPTWrapper(self._config.get("API_KEY"))