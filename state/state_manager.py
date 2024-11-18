from typing import Any


class StateManager:
    #temp
    _query: list[str]

    def __init__(self):
        self._query = []

    def get(self, key: str) -> Any:
        pass

    def update(self, key: str, value: Any):
        pass

    def get_query(self):
        return self._query

    def update_query(self, new_query:str):
        self._query.append(new_query)