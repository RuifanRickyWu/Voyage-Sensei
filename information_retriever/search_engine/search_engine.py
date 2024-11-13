from abc import ABC, abstractmethod


class SearchEngine(ABC):

    @abstractmethod
    def get_topk_poi(self, query: str, top_k: int):
        pass
