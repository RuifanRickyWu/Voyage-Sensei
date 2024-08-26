import torch
from CarTravel.Entity.poi import POI


class RankResult:
    _topk_score: torch.tensor
    _topK_index: torch.tensor
    _topk_poi: list[POI]

    def __init__(self, top_score: torch.tensor, top_index: torch.tensor):
        self._topk_score = top_score
        self._topK_index = top_index
        self._topk_poi = []

    def get_score(self):
        return self._topk_score

    def get_index(self):
        return self._topK_index

    def add_POI(self, poi):
        self._topk_poi.append(poi)

    def get_POI_list(self):
        return self._topk_poi

