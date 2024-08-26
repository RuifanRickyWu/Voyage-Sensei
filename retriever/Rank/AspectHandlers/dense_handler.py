from CarTravel.retriever.Rank.scored_POI import scored_POI
from CarTravel.data_process.embedder.STEmbedder import STEmbedder
from sklearn.metrics.pairwise import cosine_similarity
from CarTravel.LLM.GPTChatCompletion import GPTChatCompletion

class DenseHandler:
    _embedder: STEmbedder
    _gpt: GPTChatCompletion

    def __init__(self):
        self._embedder = STEmbedder()
        self._gpt = GPTChatCompletion(api_key="sk-proj-gakhZLqB54nfHKSxSmrDT3BlbkFJfdRstfPm6Vgaej1zpVY4")

    def OP_dense(self, op_aspects:list[str], scored_POIs: list[scored_POI]):
        op_aspect = self._constraint_expansion(op_aspects)
        feature_text = [" ".join(scored_POI.get_poi().get_feature()) for scored_POI in scored_POIs]
        description_text = [scored_POI.get_poi().get_description() for scored_POI in scored_POIs]

        query_embedding = self._embedder.encode(op_aspect)
        feature_embeddings = [self._embedder.encode(feature) for feature in feature_text]
        description_embeddings = [self._embedder.encode(description) for description in description_text]

        feature_similarity = self._calculate_cosine_similarity(query_embedding, feature_embeddings)
        description_similarity = self._calculate_cosine_similarity(query_embedding, description_embeddings)

        for scored_POI, feature_score, description_score in zip(scored_POIs, feature_similarity, description_similarity):
            scored_POI.set_op_score(max(feature_score, description_score))

        #aspect_embs = [self._embedder.encode(aspect) for aspect in op_aspect]
        #for scored_POI in scored_POIs:
        #    poi_embs = [self._embedder.encode(feature) for feature in scored_POI.get_poi().get_feature()]
        #    poi_embs.append(self._embedder.encode(scored_POI.get_poi().get_description()))

        #    for aspect_emb in aspect_embs:
        #        similarity = [self._calculate_cosine_similarity(aspect_emb, poi_emb) for poi_emb in poi_embs]
        #        scored_POI.set_op_score(scored_POI.get_op_score() + max(similarity))
        return scored_POIs

    def _calculate_cosine_similarity(self, query_emb, emb_list):
        # Calculate the cosine similarity between two sets of embeddings
        similarity = []
        for emb in emb_list:
            similarity.append(cosine_similarity(query_emb, emb))
        return similarity

    def _constraint_expansion(self, aspects: list[str]):
        message = (
            "consider yourself a travel recommender expand the keyword provided to a sentence that can be better converted to embeddings. "
            "For example, given words kitchen and currency exchange"
            "will be expanded to 'I want a place with kitchen and currency exchange"
            "Now the words are: '{aspects}'. Extend the words. Give me only the expanded string."
        )
        formatted_message = message.format(aspects=aspects)
        return self._gpt.make_request(formatted_message)


