import json
from jinja2 import Environment, FileSystemLoader
from intelligence.llm_client import LLMClient


class InformationRetrivalService:
    _llm_client: LLMClient
    _prompt_config : dict

    def __init__(self,prompt_config: dict, llm_client: LLMClient):
        self._prompt_config = prompt_config
        self._llm_client = llm_client

    def get_topk_poi_llm_search(self, query, top_k: int):
        template = self._load_prompt_zero_shot(query, top_k)
        result = json.loads(self._llm_client.make_request(template))
        return result

    def _load_prompt_zero_shot(self, query, top_k: int):
        #loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        #print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, k=top_k)
