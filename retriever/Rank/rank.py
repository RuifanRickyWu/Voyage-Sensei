import heapq
from CarTravel.Entity.poi import POI
from CarTravel.Entity.aspect import Indirect_Aspect
from CarTravel.retriever.Rank.scored_POI import scored_POI
from CarTravel.retriever.Rank.AspectHandlers.dense_handler import DenseHandler
from CarTravel.retriever.Rank.AspectHandlers.sparse_handler import SparseHandler
from CarTravel.retriever.Rank.AspectHandlers.indirect_aspect import IndirectAspectsHandler
from CarTravel.retriever.Rank.AspectHandlers.oc_handler import  ObjectiveConstraintHandler

class Rank:
    _sparseHandler: SparseHandler
    _denseHandler: DenseHandler
    _objectiveConstraintHandler: ObjectiveConstraintHandler

    def __init__(self):
        self._sparseHandler = SparseHandler()
        self._denseHandler = DenseHandler()
        self._indirHandler = IndirectAspectsHandler()
        self._objectiveConstraintHandler = ObjectiveConstraintHandler()

    def rank(self, oc_aspects:list[str] ,op_aspects: list[str], in_aspects: list[Indirect_Aspect], k: int):
        pois = self._objectiveConstraintHandler.filter(oc_aspects)
        scored_pois = self._initialize(pois)

        print("size after oc")
        print(len(pois))

        #apply handlers here
        #for example:
        #
        #scored_pois = OPHandler.apply_op_score(scored_pois)
        #so poi in scored_pois get op scores in its fields
        
        #scored_pois = self._indirHandler.score_indirect_aspects(in_aspects, scored_pois)

        #apply OP handlers
        #scored_pois = self._sparseHandler.OP_sparse(op_aspects, scored_pois)
        # scored_pois = self._denseHandler.OP_dense(op_aspects, scored_pois)
        return self._make_conclusion(scored_pois, k)

    def _initialize(self, pois: list[POI]):
        scored_pois = []
        for poi in pois:
            scored_pois.append(scored_POI(poi))
        return scored_pois

    def _make_conclusion(self, scored_POIs: list[scored_POI], k: int):
        poi_names = []
        for scored_POI in scored_POIs:
            
            # remove duplicate
            poi_name = scored_POI.get_poi().get_name()
            if poi_name in poi_names:
                print("poi already appeared: " + str(poi_name))
                scored_POIs.remove(scored_POI)
                continue
            else:    
                poi_names.append(poi_name)
                
            scored_POI.set_total_score(scored_POI.get_op_score() + scored_POI.get_in_score())
        topk = heapq.nlargest(k, scored_POIs, key=lambda scored_POI:scored_POI.get_total_score())
        result = []
        print("TOP POIs:")
        
        
        for scored_POI in topk:
            result.append(scored_POI.get_poi())
            print("\npoi name:")
            print(scored_POI.get_poi().get_name())
            #print("\nindirect score:")
            #print(scored_POI.get_in_score())
        return result
