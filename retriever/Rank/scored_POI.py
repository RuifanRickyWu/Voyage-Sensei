from CarTravel.Entity.poi import POI

class scored_POI:
    _POI: POI
    _op_score: float
    _in_score: float
    _total_score: float

    def __init__(self, poi: POI):
        self._POI = poi
        self._op_score = 0
        self._in_score = 0
        self._total_score = 0

    def set_op_score(self, op_score: float):
        self._op_score = op_score

    def get_op_score(self):
        return self._op_score

    def set_in_score(self, in_score: float):
        self._in_score = in_score

    def get_in_score(self):
        return self._in_score

    #might not be needed tbd
    def set_total_score(self, total_score: float):
        self._total_score = total_score

    def get_total_score(self):
        return self._total_score

    def get_poi(self):
        return self._POI