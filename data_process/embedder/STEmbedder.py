import torch
from sentence_transformers import SentenceTransformer

class STEmbedder:
    _model: SentenceTransformer

    def __init__(self):
        self._model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    def encode(self, text) -> torch.Tensor:
        if not text:
            #temporary bypass
            text = "meaningless stuff"
        return self._model.encode([text])
