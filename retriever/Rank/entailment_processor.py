from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")


class EntailmentProcessor:
    _entail: pipeline
    def __init__(self):
        self._entail = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

    def entail(self, sequence_to_classify: str, candidate:str):
        return self._entail(sequence_to_classify, candidate, multi_label=True)["scores"]
