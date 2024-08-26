import re, os, json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from CarTravel.Entity.poi import POI
from CarTravel.retriever.Rank.scored_POI import scored_POI
from CarTravel.Entity.aspect import Aspect, Indirect_Aspect
from CarTravel.data_process.embedder.embedding_processor import EmbeddingProcessor



class IndirectAspectsHandler:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.nli_tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
        self.nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
        self._embedder = EmbeddingProcessor()

    def preprocess_text(self, text: str) -> list[str]:
        """
        Preprocess text by tokenizing and converting to lowercase.
        """
        text = text.lower()
        words = re.findall(r'\w+', text)
        return words
    
    def score_indirect_aspects(self, aspects: list[Indirect_Aspect], spois: list[scored_POI]):
        '''
        Average scores across all aspects for each POI
        '''
        if aspects:
            print("started scoring process...")
            
            pois = [spoi.get_poi() for spoi in spois]
            
            accumulated_scores = torch.zeros(len(pois))
            for aspect in aspects:
                scores = self._get_aspect_scores(aspect.goals, pois)
                accumulated_scores += scores

            # Calculate the average scores across all aspects for each POI
            average_scores_across_aspects = accumulated_scores / len(aspects)
            
            for i, spoi in enumerate(spois):
                spoi.set_in_score(average_scores_across_aspects[i])
                print("poi name: " + str(spoi.get_poi().get_name()))
                print("poi indirect aspect score: " + str(spoi.get_in_score()))
                
        return spois
        
    def _get_aspect_scores(self, goals: list[str], pois: list[POI]):
        '''
        List of average similarity scores for an aspect for each POI.
        '''
        scores = torch.zeros(len(pois))
        for goal in goals:
            print("\nprocessing goal: " + str(goal) + "...\n\n")
            # goal = self._constraint_expansion(goal, query) # NOTE: decomposed goals don't get elaborated further
            scores += self._get_similarity_score_each_goal(goal, pois)
        average_scores = scores / len(goals)
        return average_scores

    def _get_similarity_score_each_goal(self, goal: str, pois: list[POI]):
        scores_for_pois = []

        goal_embedding = self._embedder.create_embedding(goal)
        goal_embedding = goal_embedding.squeeze(0)

        for poi in pois:
            # print("processing poi: " + str(poi.get_name()) + "...\n")
            #if poi.get_name() == "Hyatt Regency Toronto":
            #    print("looking at Hyatt Regency Toronto")
            #    print(f"""\tthe weight for the aspect
            #          {preference} is {weight * self._similarity_score_poi(poi.get_embedding_metrix(), query_embedding)}""")
            
            scores_for_pois.append(self._get_similarity_score_each_poi(poi.get_embedding_metrix(), goal_embedding))
        return torch.tensor(scores_for_pois)

    def _get_similarity_score_each_poi(self, emb_matrix: np.ndarray, query_embedding: torch.tensor):

        emb_matrix = torch.tensor(emb_matrix, dtype=torch.float32)
        query_embedding = torch.tensor(query_embedding, dtype=torch.float32)
        dot_product = torch.matmul(emb_matrix, query_embedding)
        norm_q = torch.norm(query_embedding)
        norm_m = torch.norm(emb_matrix, dim=1)
        norm_product = torch.where(norm_q * norm_m == 0, torch.tensor(1e-10, dtype=torch.float32), norm_q * norm_m)
        similarity = dot_product / norm_product
        return torch.mean(similarity)

    # def _constraint_expansion(self, constraint: WeightedConstraint, query: str):
    #     message = (
    #         "consider yourself a travel recommender expand the keyword provided to a sentence that can be better converted to embeddings. "
    #         "For example, the word 'Nathan Phillips Square' in 'where can I find a boutique hotel less than $200 per night near Nathan Philips square that has a rooftop bar and an outdoor pool?' "
    #         "will be expanded to 'Nathan Phillips Square, a large urban plaza in downtown Toronto'. "
    #         "Now the query is: '{query}'. Extend the word '{constraint}'. Give me only the expanded string."
    #     )
    #     formatted_message = message.format(query=query, constraint=constraint.get_constraint())
    #     constraint.set_constraint(self._gpt.make_request(formatted_message))
    #     return constraint
