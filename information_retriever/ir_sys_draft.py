import yaml
from database.database_creator import VectorDatabaseCreator
from information_retriever.embedder.tas_b_embedder import TASB

with open('/Users/rwu/dev/capstone/Car-Travel/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

print(config['RAW_POI_PATH_TEST'])
embedder = TASB()
print("check")
db_creator = VectorDatabaseCreator(config['RAW_POI_PATH_TEST'], config['VECTOR_DATABASE_PATH'], embedder)
index, map = db_creator.get_vector_database()

print(map)