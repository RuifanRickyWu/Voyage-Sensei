import json
import logging
from datetime import date

from web_search_processor.web_search_client import WebSearchClient
from intelligence.llm_agent import LLMAgent
from state.state_entity.POI import POI
from jinja2 import Environment, FileSystemLoader


class EventProcessorClient:
    _web_search_client: WebSearchClient
    _llm_agent: LLMAgent
    _env: Environment

    def __init__(self, llm_agent: LLMAgent, web_search_client: WebSearchClient, prompt_config: dict):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._llm_agent = llm_agent
        self._web_search_client = web_search_client
        self._prompt_config = prompt_config
        self._env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))

    def web_search_single_poi_for_event(self, poi: POI):
        current_date = date.today().strftime("%Y-%m-%d")
        query_general = "event for " + poi.get_poi().get("name") + "on " + current_date
        search_result_general = self._parse_web_search_results(self._web_search_client.google_search(query_general, 2))
        query_ticket_master = "event for " + poi.get_poi().get("name") + "on " + current_date + "ticket_master"
        search_result_ticket_master = self._parse_web_search_results(self._web_search_client.google_search(query_ticket_master, 2))
        self.logger.info(f"Current Search Result -> : {search_result_general + search_result_ticket_master }")
        return search_result_general + search_result_ticket_master

    def llm_summarize_event(self, poi: POI, event_search_result: json):
        template = self._load_prompt_event(poi.get_poi().get("name"), date.today().strftime("%Y-%m-%d"), event_search_result)
        result = self._llm_agent.make_request(template)
        event_result = json.loads(result)
        return event_result

    def _parse_web_search_results(self, search_results):
        if not search_results or "items" not in search_results:
            return "No related results"

        output = []
        for item in search_results["items"]:
            title = item["title"]
            link = item["link"]
            snippet = item.get("snippet", "No Summary")
            output.append(f"**{title}**\n{snippet}\n[link]({link})\n")
        return "\n".join(output)

    def _load_prompt_event(self, poi_name:str, date,  event_search_result: json):
        template = self._env.get_template(self._prompt_config.get("EVENT_SUMMARIZATION"))
        return template.render(poi_name = poi_name, date = date, event_search_result = event_search_result)