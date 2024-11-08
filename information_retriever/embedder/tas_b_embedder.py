import torch
from information_retriever.embedder.embedder import Embedder
from sentence_transformers import SentenceTransformer


class TASB(Embedder):
    _model: SentenceTransformer

    def __init__(self):
        super().__init__()
        _model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    def embed(self, text: list[str]) -> torch.tensor:
        return self._model.encode(text)
