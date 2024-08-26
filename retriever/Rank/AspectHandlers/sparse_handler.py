from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import nltk
from CarTravel.retriever.Rank.scored_POI import scored_POI


class SparseHandler:
    def __init__(self):
        nltk.download('punkt')

    def OP_sparse(self, op_aspect:list[str], scored_POIs: list[scored_POI]):
        op_aspect = " ".join(op_aspect)
        tokenized_query = word_tokenize(op_aspect.lower())

        feature_text = [" ".join(scored_POI.get_poi().get_feature()) for scored_POI in scored_POIs]
        description_text = [scored_POI.get_poi().get_description() for scored_POI in scored_POIs]
        feature_tokenized_documents = [word_tokenize(text.lower()) for text in feature_text]
        description_tokenized_documents = [word_tokenize(text.lower()) for text in description_text]

        bm25_feature = BM25Okapi(feature_tokenized_documents)
        bm25_description = BM25Okapi(description_tokenized_documents)
        feature_scores = bm25_feature.get_scores(tokenized_query)
        description_scores= bm25_description.get_scores(tokenized_query)

        for scored_POI, feature_score, description_score in zip(scored_POIs, feature_scores, description_scores):
            scored_POI.set_op_score(max(feature_score, description_score))
        return scored_POIs