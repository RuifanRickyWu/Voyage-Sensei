from CarTravel.retriever.Rank.entailment_processor import EntailmentProcessor
from CarTravel.retriever.Rank.scored_POI import scored_POI
from Ca
class IndirectEntailmentHandle:
    _entail: EntailmentProcessor
    def __init__(self):
        self._entail = EntailmentProcessor()

    def indirect_entailment(self, scored_poi: list[scored_POI], ):
        return

