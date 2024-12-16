import json
from jinja2 import Environment, FileSystemLoader
from intelligence.llm_agent import LLMAgent
from state.state_manager import StateManager
from state.state_entity.POI import POI


class InformationRetrievalClient:
    _llm_agent: LLMAgent
    _prompt_config: dict

    def __init__(self, llm_agent: LLMAgent, prompt_config: dict, ):
        self._prompt_config = prompt_config
        self._llm_agent = llm_agent

    def llm_search_get_top_k_poi(self, state_manager: StateManager, top_k: int):
        queries = state_manager.get_query()
        template = self._load_prompt_zero_shot(queries, top_k)
        llm_result = json.loads(self._llm_agent.make_request(template))
        self._load_llm_result_to_search_result(llm_result, state_manager)
        return llm_result

    def _load_prompt_zero_shot(self, query, top_k: int):
        # loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        # print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, k=top_k)

    def _load_llm_result_to_search_result(self, llm_result: json, state_manager: StateManager):
        poi_list = []
        for result in llm_result:
            poi_list.append(POI(
                name= result.get("name"),
                address= result.get("address"),
                description= result.get("description"),
                duration = result.get("duration")
            ))
        print(poi_list)


