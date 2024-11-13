from abc import abstractmethod, ABC

class Planner(ABC):

    @abstractmethod
    def plan(self, query:str, poi_list: dict):
        pass
