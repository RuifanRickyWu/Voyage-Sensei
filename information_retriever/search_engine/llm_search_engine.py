from intelligence.wrapper.llm_wrapper import LLMWrapper
from jinja2 import Environment, FileSystemLoader


class LLMSearchEngine:
    _agent: LLMWrapper
    _prompt_config: dict

    def __init__(self, agent: LLMWrapper, prompt_config: dict):
        self._agent = agent
        self._prompt_config = prompt_config

    #Get k poi from GPT
    def get_topk_poi(self, query, top_k: int):
        template = self._load_prompt(query, top_k)
        print(template)
        return self._agent.make_request(template)

    def _load_prompt(self, query, top_k: int):
        #loading 0_shot_prompt for baseline
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # Load the template file
        #print(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        template = env.get_template(self._prompt_config.get("BASELINE_ZEROSHOT_PROMPT"))
        return template.render(user_query=query, k=top_k)
