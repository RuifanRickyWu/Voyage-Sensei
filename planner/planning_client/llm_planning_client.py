import json
from jinja2 import Environment, FileSystemLoader
from state.state_manager import StateManager
from state.state_entity.POI import POI
from state.state_entity.current_plan import CurrentPlan
from intelligence.llm_agent import LLMAgent


class LLMPlanningClient:
    _llm_agent: LLMAgent
    _prompt_config: dict

    def __init__(self, llm_agent: LLMAgent, prompt_config: dict):
        self._llm_agent = llm_agent
        self._prompt_config = prompt_config

    def llm_planning(self, state_manager: StateManager, queries: list[str], poi_list: list[str]):
        template = self._load_prompt_zeroshot(queries, poi_list)
        #result is a poi sequence list
        result = json.loads(self._llm_agent.make_request(template))
        self._create_current_plan_with_hardcord_starting_point(state_manager, result)

    def llm_planning_after_critique(self, state_manager: StateManager, queries: list[str], poi_list: list[str], critiques: list[str]):
        template = self._load_prompt_zeroshot_after_critique(queries, critiques, poi_list)
        #result is a poi sequence list
        result = json.loads(self._llm_agent.make_request(template))
        self._create_current_plan_with_hardcord_starting_point(state_manager, result)

    def _load_prompt_zeroshot(self, query: list[str], poi_list: list[str]):
        #loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        #print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, pois=poi_list)

    def _load_prompt_zeroshot_after_critique(self, query: list[str], critique: list[str], poi_list: list[str]):
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_AFTER_CRITIQUE_PROMPT"))
        return template.render(user_query=query, critique=critique, pois=poi_list)

    def _create_current_plan_with_hardcord_starting_point(self, state_manager: StateManager, result: dict):
        starting_point = POI(
            name= "Starting Point",
            address= "21 Carlton St, Toronto, ON M5B 1L3, Canada",
            description= "Starting and Ending Point"
        )
        poi_in_sequence = [starting_point]
        current_search_list = state_manager.get_current_search_result().get_retrieved_poi_list()
        for poi_name in result:
            for poi in current_search_list:
                if poi.get_poi().get("name") == poi_name:
                    poi_in_sequence.append(poi)
        poi_in_sequence.append(starting_point)
        state_manager.update_current_plan(CurrentPlan(poi_in_sequence))

