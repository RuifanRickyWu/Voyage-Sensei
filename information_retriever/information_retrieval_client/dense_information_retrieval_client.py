import faiss
from information_retriever.database.vector_database_creator import VectorDatabaseCreator


class DenseInformationRetrievalClient:
    _index: faiss.Index
    _embID_to_poi_mapping: dict

    def __init__(self, vectorDB_creator: VectorDatabaseCreator):
        self._index, self._embID_to_poi_mapping = vectorDB_creator.get_vector_database()
