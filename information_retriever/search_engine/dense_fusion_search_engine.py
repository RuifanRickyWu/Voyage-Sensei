from information_retriever.search_engine.search_engine import SearchEngine
from information_retriever.embedder.embedder import Embedder


class DenseFusionSearchEngine(SearchEngine):
    _embedder: Embedder

    def __init__(self, embedder: Embedder):
        self._embedder = embedder

    def get_topk_poi(self, query: str, top_k: int):
        pass
