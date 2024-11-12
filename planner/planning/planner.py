from abc import abstractmethod, ABC


class Planner(ABC):

    @abstractmethod
    def plan(self):
        pass
