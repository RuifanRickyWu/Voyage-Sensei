import torch
from information_retriever.embedder.embedder import Embedder
from sentence_transformers import SentenceTransformer


class TASB(Embedder):
    _model: SentenceTransformer

    def __init__(self):
        self._model = SentenceTransformer("paraphrase-MiniLM-L6-v2", device="cpu")

    def embed(self, texts: list[str]) -> list[torch.Tensor]:
        embeddings = []
        for text in texts:
            embeddings.append(torch.tensor(self._model.encode(text)))
        return embeddings
