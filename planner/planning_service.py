from planner.planning.llm_planner import LLMPlanner
from intelligence.llm_client import LLMClient
from jinja2 import Environment, FileSystemLoader

class PlanningService:
    _prompt_config: dict
    _llm_client: LLMClient
    _llm_planner: LLMPlanner

    def __init__(self, prompt_config: dict, llm_client: LLMClient):
        self._llm_client = llm_client
        self._prompt_config = prompt_config

    def plan(self, query, poi_list: dict):
        return self._llm_planner.plan(query, poi_list)

    def plan_with_llm_planner(self, query:str, poi_list: dict):
        template = self._load_prompt_zeroshot(query, poi_list)
        return self._llm_client.make_request(template)

    def _load_prompt_zeroshot(self, query:str, poi_list:dict):
        #loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        #print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, pois = poi_list)
