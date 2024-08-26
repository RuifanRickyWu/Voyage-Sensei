import numpy as np
import re
import torch
from CarTravel.retriever.Rank.preference_matching import PreferenceMatching
from CarTravel.Entity.poi import POI
from CarTravel.retriever.Rank.scored_POI import scored_POI
from CarTravel.Entity.rank_result import RankResult
from CarTravel.retriever.Rank.weighted_constraint import WeightedConstraint


class TradeOff:
    _matcher: PreferenceMatching

    def __init__(self):
        self._matcher = PreferenceMatching()

    def get_topk_poi_dynamic_weights(self, original_query, pois: list[POI], k: int):
        weighted_constraints = self._get_weighted_constraints(original_query)

        for con in weighted_constraints:
            print(f"\tone aspect weight for query '{con.get_constraint()}' is {con.get_weight()}\n")

        score = torch.zeros(len(pois))
        score = score + self._matcher.get_preference_score(original_query, weighted_constraints, pois)
        # further trade off analysis

        #print(f"\ncurrently in get_topk_poi. score is\n{score}\n")

        # get the index
        top_val, top_indices = score.topk(k)

        #print(f"the value of top_val is {top_val} while the value of top_indices is {top_indices}")

        result = RankResult(top_val, top_indices)
        for index in top_indices:
            poi = pois[index.item()]
            result.add_POI(poi)
        return result

    def _get_weighted_constraints(self, original_query:str):

        weights = self._matcher.generate_weights(original_query)
        weights_as_list = re.split(r'\), \(', weights)

        # Remove leading '(' from the first element and trailing ')' from the last element
        weights_as_list[0] = weights_as_list[0][1:]
        weights_as_list[-1] = weights_as_list[-1][:-1]

        # Regular expression to match each tuple
        pattern = re.compile(r'\(([^,]+), ([^)]+)\)')

        # Convert each substring to a tuple using regex
        constraint_list = []
        for item in weights_as_list:
            match = pattern.match(f"({item})")
            if match:
                constraint = match.group(1).strip()
                weight = float(match.group(2).strip())
                constraint_list.append(WeightedConstraint(constraint, weight))

        return constraint_list

    def rank(self, pois: list[POI], original_query: str, k: int):
        scored_pois = []
        for poi in pois:
            scored_pois.append(scored_POI(poi))

        #apply handlers here
        #for example:
        #
        #scored_pois = OPHandler.apply_op_score(scored_pois)
        #so poi in scored_pois get op scores in its fields




