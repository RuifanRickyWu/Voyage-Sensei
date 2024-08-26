class WeightedConstraint:
    _constraint: str
    _weight: float

    def __init__(self, constraint: str, weight: float):
        self._weight = weight
        self._constraint = constraint

    def get_constraint(self):
        return self._constraint

    def get_weight(self):
        return self._weight

    def set_constraint(self, constraint:str):
        self._constraint=constraint
