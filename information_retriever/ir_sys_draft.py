import yaml
from database.database_creator import VectorDatabaseCreator

with open('/Users/rwu/dev/capstone/Car-Travel/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

print(config['RAW_POI_PATH_TEST'])

db_creator = VectorDatabaseCreator(config['RAW_POI_PATH_TEST'], config['VECTOR_DATABASE_PATH'])
db_creator.create_vector_database()