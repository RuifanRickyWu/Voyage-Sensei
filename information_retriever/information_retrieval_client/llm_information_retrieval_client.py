import json
import logging

from jinja2 import Environment, FileSystemLoader
from intelligence.llm_agent import LLMAgent
from state.state_manager import StateManager
from state.state_entity.POI import POI
from state.state_entity.current_search import CurrentSearch


class LLMInformationRetrievalClient:
    _llm_agent: LLMAgent
    _prompt_config: dict

    def __init__(self, llm_agent: LLMAgent, prompt_config: dict):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._prompt_config = prompt_config
        self._llm_agent = llm_agent

    def llm_search_get_top_k_poi(self, state_manager: StateManager, top_k: int):
        queries = state_manager.get_query()
        template = self._load_prompt_zero_shot(queries, top_k)
        #be caucious, changing model may change the output.
        result = self._llm_agent.make_request(template)
        self.logger.debug(f"The result from llm for ir is {result}")
        llm_search_result = json.loads(result)
        self._load_llm_result_to_search_result(llm_search_result, state_manager)

    def llm_search_with_critique(self, state_manager: StateManager):
        queries = state_manager.get_query()
        critiques = state_manager.get_critique()
        current_poi_list = state_manager.get_current_plan().get_converted_planned_poi_list()
        template = self._load_prompt_with_critique_zero_shot(queries, critiques, current_poi_list)
        #be caucious, changing model may change the output.
        result = self._llm_agent.make_request(template)
        self.logger.info(f"The result from llm for ir is {result}")
        llm_search_result = json.loads(result)
        self._load_llm_result_to_search_result(llm_search_result, state_manager)

    def _load_prompt_zero_shot(self, query, top_k: int):
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, k=top_k)

    def _load_prompt_with_critique_zero_shot(self, query, critiques, current_poi_list):
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        template = env.get_template(self._prompt_config.get("BASELINE_AFTER_CRITIQUE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, current_pois = current_poi_list, critiques = critiques)

    def _load_llm_result_to_search_result(self, llm_result: json, state_manager: StateManager):
        print(llm_result)
        poi_list = []
        for result in llm_result:
            poi_list.append(POI(
                name= result.get("name"),
                address= result.get("address"),
                description= result.get("description"),
                duration = result.get("duration")
            ))
        state_manager.update_current_search_result(CurrentSearch(poi_list))



