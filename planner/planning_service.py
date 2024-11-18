from planner.planning.llm_planner import LLMPlanner

class PlanningService:
    _llm_planner: LLMPlanner

    def __init__(self, llm_planner: LLMPlanner):
        self._llm_planner = llm_planner

    def plan_with_llm_planner(self, query, poi_list: dict):
        return self._llm_planner.plan(query, poi_list)
