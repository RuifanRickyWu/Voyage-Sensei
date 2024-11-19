from typing import Any


class StateManager:
    #temp
    _query: list[str]
    _current_plan: list[dict]

    def __init__(self):
        self._query = []
        self._current_plan = None

    def get(self, key: str) -> Any:
        pass

    def update(self, key: str, value: Any):
        pass

    def get_query(self):
        return self._query

    def update_query(self, new_query: str):
        self._query.append(new_query)

    def get_current_plan(self):
        return self._current_plan

    def update_current_plan(self, plan: list[dict]):
        self._current_plan = plan
