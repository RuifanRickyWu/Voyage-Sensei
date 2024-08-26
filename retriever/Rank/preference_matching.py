import torch
import numpy as np

from CarTravel.data_process.embedder.embedding_processor import EmbeddingProcessor
from CarTravel.Entity.poi import POI
from CarTravel.LLM.GPTChatCompletion import GPTChatCompletion
from CarTravel.retriever.Rank.weighted_constraint import WeightedConstraint
from CarTravel.config import API_KEY


class PreferenceMatching:
    _embedder = EmbeddingProcessor
    _gpt = GPTChatCompletion

    def __init__(self):
        self._embedder = EmbeddingProcessor()
        self._gpt = GPTChatCompletion(api_key=API_KEY)

    def get_preference_score(self, query: str, constraints: list[WeightedConstraint], pois: list[POI]):
        score = torch.zeros(len(pois))
        for constraint in constraints:
            constraint = self._constraint_expansion(constraint, query)
            score = score + self._get_similarity_score_each_constraint_weighted(constraint, pois)
        return score

    def _get_similarity_score_each_constraint_weighted(self, weighted_constraint: WeightedConstraint, pois: list[POI]):
        similarity = []
        preference = weighted_constraint.get_constraint()  #when we say query we actually mean preference
        weight = weighted_constraint.get_weight()

        query_embedding = self._embedder.create_embedding(preference)
        query_embedding = query_embedding.squeeze(0)

        for poi in pois:
            #if poi.get_name() == "Hyatt Regency Toronto":
            #    print("looking at Hyatt Regency Toronto")
            #    print(f"""\tthe weight for the aspect
            #          {preference} is {weight * self._similarity_score_poi(poi.get_embedding_metrix(), query_embedding)}""")
            similarity.append(weight * (self._similarity_score_poi(poi.get_embedding_metrix(), query_embedding)))
        return torch.tensor(similarity)

    def _similarity_score_poi(self, emb_matrix: np.ndarray, query_embedding: torch.tensor):

        emb_matrix = torch.tensor(emb_matrix, dtype=torch.float32)
        query_embedding = torch.tensor(query_embedding, dtype=torch.float32)
        dot_product = torch.matmul(emb_matrix, query_embedding)
        norm_q = torch.norm(query_embedding)
        norm_m = torch.norm(emb_matrix, dim=1)
        norm_product = torch.where(norm_q * norm_m == 0, torch.tensor(1e-10, dtype=torch.float32), norm_q * norm_m)
        similarity = dot_product / norm_product
        return torch.mean(similarity)

    def _constraint_expansion(self, constraint: WeightedConstraint, query: str):
        message = (
            "consider yourself a travel recommender expand the keyword provided to a sentence that can be better converted to embeddings. "
            "For example, the word 'Nathan Phillips Square' in 'where can I find a boutique hotel less than $200 per night near Nathan Philips square that has a rooftop bar and an outdoor pool?' "
            "will be expanded to 'Nathan Phillips Square, a large urban plaza in downtown Toronto'. "
            "Now the query is: '{query}'. Extend the word '{constraint}'. Give me only the expanded string."
        )
        formatted_message = message.format(query=query, constraint=constraint.get_constraint())
        constraint.set_constraint(self._gpt.make_request(formatted_message))
        return constraint

    def generate_weights(self, query: str):
        prompt = f"""
        Given a request for a hotel, extract the various hotel aspects that the user is asking for, and find the relative importance of each aspect by giving it weight between 0 and 1. The sum of all the weights must be equal to 1.
        The value of a weight should be dependent on the sentiment shown by the user. Phrases like "Find me a place with aspect X" should cause aspect X to have a higher weight than phrases like: "I would prefer a place with aspect X".

        ##Example
        Input: find me a hotel that is near Nathan Phillips square in Toronto and has free wifi. The Hotel must be under 300 dollars a night, and is ideally not much more than 200 dollars a night.
        Output: (near Nathan Phillips square, 0.1), (free wifi, 0.2), (under 300 dollars, 0.5), (cheap, 0.2)

        Input: {query}
        Output:
        """
        return self._gpt.make_request(prompt)
