from state.state_manager import StateManager
from information_retriever.information_retrieval_client import InformationRetrievalClient


class InformationRetrievalService:
    _information_retrieval_client: InformationRetrievalClient

    def __init__(self, information_retrieval_client: InformationRetrievalClient):
        self._information_retrieval_client = information_retrieval_client

    def llm_search_get_top_k(self, state_manager: StateManager, top_k: int):
        return self._information_retrieval_client.llm_search_get_top_k_poi(state_manager, top_k)
