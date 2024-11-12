from abc import ABC, abstractmethod
from information_retriever.search_engine.search_engine import SearchEngine
from information_retriever.search_engine.llm_search_engine import LLMSearchEngine
from intelligence.wrapper.llm_wrapper import LLMWrapper
from intelligence.singleton_llm_agent import SingletonLLMAgent


class IRFactory(ABC):

    @abstractmethod
    def create_search_engine(self) -> SearchEngine:
        pass


class LLMBasedIRFactory(IRFactory):
    _config: dict

    def __init__(self, config: dict):
        self._config = config

    def _get_llm_agent(self) -> LLMWrapper:
        instance = SingletonLLMAgent(self._config)
        return instance.get_agent()

    def create_search_engine(self) -> LLMSearchEngine:
        search_engine = LLMSearchEngine(self._get_llm_agent())
        return search_engine
