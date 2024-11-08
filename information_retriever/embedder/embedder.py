from abc import ABC, abstractmethod

class Embedder(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def embed(self, text: list[str]):
        pass