import json
import os
import faiss
from information_retriever.embedder.tas_b_embedder import Embedder


class VectorDatabaseCreator:
    _raw_poi_path: str
    _output_path: str
    _id_poi_info_map: dict
    _embedder: Embedder
    _total_review: int

    def __init__(self, raw_poi_path: str, output_path: str, embedder: Embedder):
        self._raw_poi_path = raw_poi_path
        self._output_path = output_path
        self._embedder = embedder

    def get_vector_database(self):

        if self._output_path is not None and os.path.exists(self._output_path):
            index = faiss.read_index(self._output_path)
            return index, self._id_poi_info_map
        else:
            dimension_size = 768
            index = self._load_index_with_poi_list(faiss.IndexFlatIP(dimension_size))
        return index, self._id_poi_info_map


    def _load_index_with_poi_list(self, index):
        temp_id_poi_info_map = {}
        temp_total_review = 0
        id = 1

        for filename in os.listdir(self._raw_poi_path):
            if os.path.isfile(os.path.join(self._raw_poi_path, filename)) and filename != ".DS_Store":
                print("Processing POI " + filename)

                with open(os.path.join(self._raw_poi_path, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                review_list = [item["text"][0] for item in data['reviews'] if "text" in item]
                #add describption back
                #self._embedder.embed(review_list)
                print("check1")
                embeddings = self._embedder.embed(review_list)
                print("check2")
                for embedding in embeddings:
                    index.add(embedding)

                info = {}
                info['name'] = filename
                info['review_size'] = len(review_list)
                temp_id_poi_info_map[id] = info
                temp_total_review += len(review_list)
                id += 1

        self._total_review = temp_total_review
        self._id_poi_info_map = temp_id_poi_info_map
        #faiss.write_index(index, self._output_path)

        return index, self._id_poi_info_map
