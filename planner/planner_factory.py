from abc import ABC, abstractmethod
from intelligence.singleton_llm_agent import SingletonLLMAgent
from intelligence.wrapper.llm_wrapper import LLMWrapper
from planner.planning.planner import Planner
from planner.planning.llm_planner import LLMPlanner

class PlannerFactory(ABC):

    @abstractmethod
    def create_planner(self) -> Planner:
        pass



class LLMPlannerFactory(PlannerFactory):
    _config: dict

    def __init__(self,config: dict):
        self._config = config

    def _get_llm_agent(self) -> LLMWrapper:
        instance = SingletonLLMAgent(self._config)
        return instance.get_agent()

    def create_planner(self) -> Planner:
        planner = LLMPlanner(self._get_llm_agent())
        return planner

