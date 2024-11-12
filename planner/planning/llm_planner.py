from planner.planning.planner import Planner
from intelligence.wrapper.llm_wrapper import LLMWrapper


class LLMPlanner(Planner):
    _agent: LLMWrapper

    def __init__(self, agent: LLMWrapper):
        self._agent = agent

    def plan(self):
        pass
