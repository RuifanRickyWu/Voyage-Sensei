import json
import logging

from jinja2 import Environment, FileSystemLoader
from intelligence.llm_agent import LLMAgent
from state.state_manager import StateManager
from state.state_entity.POI import POI
from state.state_entity.current_search import CurrentSearch


class CritiqueClient:
    _llm_agent: LLMAgent
    _prompt_config: dict

    def __init__(self, llm_agent: LLMAgent, prompt_config: dict):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._prompt_config = prompt_config
        self._llm_agent = llm_agent

    def identify_and_remove_critiqued_poi(self, state_manager:StateManager):
        critiques = state_manager.get_critique()
        current_poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        template = self._load_prompt_zero_shot(critiques, current_poi_list)
        result = self._llm_agent.make_request(template)
        self.logger.info(f"The list with POI removed is {result}")
        undesired_poi_list = json.loads(result)
        self._remove_undesired_poi(state_manager, undesired_poi_list)

    def _load_prompt_zero_shot(self, critiques, current_poi_list):
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        template = env.get_template(self._prompt_config.get("CRITIQUE_RESOLUTION_PROMPT"))
        return template.render(critiques = critiques, poi_sequence = current_poi_list)

    def _remove_undesired_poi(self, state_manager: StateManager, undesired_poi_result: dict):
        poi_list = state_manager.get_current_plan().get_poi_in_sequence()
        for undesired_poi in undesired_poi_result:
            for poi in poi_list:
                if undesired_poi.get("name") == poi.get_poi().get("name"):
                    poi_list.remove(poi)
        state_manager.get_current_plan().update_poi_in_sequence(poi_list)



