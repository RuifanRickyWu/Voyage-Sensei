from state.state_manager import StateManager
from information_retriever.information_retrieval_client.llm_information_retrieval_client import LLMInformationRetrievalClient


class InformationRetrievalService:
    _information_retrieval_client: LLMInformationRetrievalClient

    def __init__(self, information_retrieval_client: LLMInformationRetrievalClient):
        self._information_retrieval_client = information_retrieval_client

    def llm_search_get_top_k(self, state_manager: StateManager, top_k: int):
        self._information_retrieval_client.llm_search_get_top_k_poi(state_manager, top_k)

    def llm_search_during_critique(self, state_manager: StateManager):
        self._information_retrieval_client.llm_search_with_critique(state_manager)
