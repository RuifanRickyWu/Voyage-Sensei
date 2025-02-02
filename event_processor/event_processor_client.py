import json
import logging
from datetime import date

from web_search_processor.web_search_client import WebSearchClient
from intelligence.llm_agent import LLMAgent
from state.state_entity.POI import POI


class EventProcessorClient:
    _web_search_client: WebSearchClient
    _llm_agent: LLMAgent

    def __init__(self, llm_agent: LLMAgent, web_search_client: WebSearchClient):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._llm_agent = llm_agent
        self._web_search_client = web_search_client

    def web_search_single_poi_for_event(self, poi: POI):
        current_date = date.today().strftime("%Y-%m-%d")
        query = "event for " + poi.get_poi().get("name") + "on " + current_date
        search_result = self._parse_web_search_results(self._web_search_client.google_search(query, 3))
        self.logger.info(f"Current Search Result -> : {search_result}")
        return search_result

    def llm_summarize_event(self, poi: POI, search_result: json):
        pass

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
