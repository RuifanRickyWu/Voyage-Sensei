from abc import ABC, abstractmethod

class Embedder(ABC):
    def __init__(self):
        pass

    def embed(self, text: list[str]):
        pass