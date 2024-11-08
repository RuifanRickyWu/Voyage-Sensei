import json
import os
import faiss


class VectorDatabaseCreator:
    _raw_poi_path: str
    _output_path: str
    _id_poi_info_map: map

    def __init__(self, raw_poi_path: str, output_path: str):
        self._raw_poi_path = raw_poi_path
        self._output_path = output_path

    def create_vector_database(self):
        temp_id_poi_info_map = {}
        id = 1
        index = self._create_index()

        for filename in os.listdir(self._raw_poi_path):
            if os.path.isfile(os.path.join(self._raw_poi_path, filename)):
                print("Processing POI " + filename)

                with open(os.path.join(self._raw_poi_path, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)

        print(len(data['reviews']))

        return None

    def _create_index(self):
        if self._output_path is not None and os.path.exists(self._raw_poi_path):
            index = faiss.read_index(self._output_path)
        else:
            dimension_size = 768
            index = faiss.IndexFlatIP(dimension_size)
        return index
