import json

from information_retriever.search_engine.llm_search_engine import LLMSearchEngine


class InformationRetrivalService:
    _llm_search_engine: LLMSearchEngine

    def __init__(self, llm_search_engine):
        self._llm_search_engine = llm_search_engine

    def get_topk_poi_llm_search(self, query, top_k: int):
        return json.loads(self._llm_search_engine.get_topk_poi(query, top_k))
