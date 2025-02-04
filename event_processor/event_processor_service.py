from event_processor.event_processor_client import EventProcessorClient
from state.state_manager import StateManager


class EventProcessorService:
    _event_processor_client: EventProcessorClient

    def __init__(self, event_processor_client: EventProcessorClient):
        self._event_processor_client = event_processor_client

    def search_for_event(self, state_manager: StateManager):
        poi_list = state_manager.get_current_search_result().get_retrieved_poi_list()
        for poi in poi_list:
            event_search_result = self._event_processor_client.web_search_single_poi_for_event(poi)
            poi.update_event_info(self._event_processor_client.llm_summarize_event(poi, event_search_result))
            debug = poi.get_poi().get("event")
            print(debug)

