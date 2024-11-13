from planner.planning.planner import Planner
from intelligence.wrapper.llm_wrapper import LLMWrapper
from jinja2 import Environment, FileSystemLoader


class LLMPlanner(Planner):
    _agent: LLMWrapper
    _prompt_config: dict

    def __init__(self, agent: LLMWrapper, prompt_config: dict):
        self._agent = agent
        self._prompt_config = prompt_config

    def plan(self, query:str, poi_list: dict):
        template = self._load_prompt(query, poi_list)
        print(template)
        return self._agent.make_request(template)

    def _load_prompt(self, query:str, poi_list:dict):
        #loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, pois = poi_list)