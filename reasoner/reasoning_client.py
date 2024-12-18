import json

from jinja2 import Environment, FileSystemLoader

from intelligence.llm_agent import LLMAgent
from state.state_manager import StateManager


class ReasoningClient:

    _llm_agent: LLMAgent
    _prompt_config: dict
    _env: Environment

    def __init__(self, llm_agent: LLMAgent, prompt_config: dict):
        self._llm_agent = llm_agent
        self._prompt_config = prompt_config
        self._env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))


    def keyword_summarization_for_poi(self, state_manager: StateManager, poi_list: list[str], queries: list[str]):
        template = self._load_prompt_poi_keyword(poi_list, queries)
        keyword_summary_result = json.loads(self._llm_agent.make_request(template))
        self._load_keywords_for_planned_poi(state_manager, keyword_summary_result)


    def _load_prompt_poi_keyword(self, poi_list: list[str], queries: list[str]):
        template = self._env.get_template(self._prompt_config.get("POI_KEYWORD_SUMMARIZATION"))
        return template.render(poi_list = poi_list, queries = queries)

    def _load_keywords_for_planned_poi(self, state_manager: StateManager, keyword_result: dict):
        poi_list = state_manager.get_current_plan().get_poi_in_sequence()
        for keyword_unit in keyword_result:
            for poi in poi_list:
                if poi.get_poi().get('name') == keyword_unit.get('poi'):
                    poi.update_keywords(keyword_unit.get('keywords'))
        state_manager.get_current_plan().update_poi_in_sequence(poi_list)



    def trip_summary(self, state_manager: StateManager, queries: list[str], poi_list: list[str]):
        template = self._load_prompt_trip_summary(queries, poi_list)
        trip_summary_result = self._llm_agent.make_request(template)
        state_manager.get_current_plan().update_summary(trip_summary_result)

    def _load_prompt_trip_summary(self, queries: list[str], poi_list: list[str]):
        template = self._env.get_template(self._prompt_config.get("TRIP_SUMMARIZATION"))
        return template.render(poi_list = poi_list, queries = queries)