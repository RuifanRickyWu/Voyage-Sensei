import json

import numpy as np
import whoosh.index
from whoosh.index import create_in, open_dir
import os
from whoosh.qparser import MultifieldParser
from whoosh.query import And
from CarTravel.Entity.poi import POI
from CarTravel.data_process.embedder.embedding_processor import EmbeddingProcessor

class ObjectiveConstraintHandler:
    _index: whoosh.index.FileIndex
    _raw_data_dir: str
    _processor: EmbeddingProcessor
    _all_poi: list[POI]

    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), '../../../data_process/database/hotel_db')
        if os.path.exists(db_path):
            self._index = open_dir(db_path)
        self._raw_data_dir = os.path.join(os.path.dirname(__file__), '../../../data_process/database/hotel_data_new')
        self._processor = EmbeddingProcessor()
        self._all_poi = []

    def _query(self, constraint_list: list[str]):
        pois = []
        fields = ["name", "features", "description"]
        qparse = MultifieldParser(fields, self._index.schema)

        if not constraint_list:
            raise ValueError("The constraint_list cannot be empty.")

        with self._index.searcher() as searcher:
            if len(constraint_list) == 1:
                query = qparse.parse(constraint_list[0])
            else:
                queries = [qparse.parse(constraint) for constraint in constraint_list]
                query = And(queries)

            results = searcher.search(query, limit=None)
            for result in results:
                embedding_strings = result.get('embedding_matrix').split('|')
                embedding_metrix = np.stack([np.array(list(map(float, emb_str.split(',')))) for emb_str in embedding_strings])

                pois.append(POI(result.get('id', None),
                                result.get('name', None),
                                result.get('description', None),
                                result.get('features', None),
                                embedding_metrix
                                #result.get('geojson', None)))
                                ))
            return pois

    def filter(self, oc_aspects:list[str]):
        if not oc_aspects:
            if len(self._all_poi) == 0:
                print("check")
                self._load_all()
            return self._all_poi
        return self._query(oc_aspects)

    def _load_all(self):
        id = 0
        for filename in os.listdir(self._raw_data_dir):
            if os.path.isfile(os.path.join(self._raw_data_dir, filename)):
                print(filename)
                with open(os.path.join(self._raw_data_dir, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                basic_data = data['basic_data']
                name = basic_data.get('name', None),
                description = data.get('description', None),
                feature = ', '.join(data.get('featues', [])),
                reviews = data.get('reviews', [])

                self._all_poi.append(POI(id = str(id),
                                name = name,
                                description= description,
                                feature= feature,
                                embedding_metrix= self._processor.create_and_load_hotel_embedding_real_time(name, feature, description, reviews)
                ))
