import json

import whoosh.index
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC
import os
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser
from whoosh.query import Or
from CarTravel.Entity.poi import POI
from CarTravel.data_process.embedder.embedding_processor import EmbeddingProcessor
from CarTravel.data_process.geo.geo_encode import GeoEncode

class WhooshDB:
    _schema: Schema
    _index: whoosh.index.FileIndex
    _processor: EmbeddingProcessor
    _geo_processor: GeoEncode
    def __init__(self):
        self._processor = EmbeddingProcessor()
        self._geo_processor = GeoEncode()
        db_path = os.path.join(os.path.dirname(__file__), "database", "hotel_db")
        if os.path.exists(db_path):
            self._index = open_dir(db_path)
        self._schema = Schema(
            id=TEXT(stored=True),
            PoiType=TEXT(stored=True),
            name=TEXT(stored=True),
            url=ID(stored=True, unique=True),
            priceRange=TEXT(stored=True),
            ratingValue=NUMERIC(stored=True),
            reviewCount=NUMERIC(stored=True),
            streetAddress=TEXT(stored=True),
            addressLocality=TEXT(stored=True),
            postalCode=TEXT(stored=True),
            addressCountry=TEXT(stored=True),
            image=TEXT(stored=True),
            description=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            features=TEXT(stored=True, analyzer=StemmingAnalyzer()),

            review_title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            review_text=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            review_rate=NUMERIC(stored=True),
            review_tripDate=TEXT(stored=True),

            embedding_matrix=TEXT(stored=True),

            geojson=TEXT(stored=True)

        )

    def create_and_load_hotel_index(self):

        database_path = os.path.join(os.path.dirname(__file__), 'database', 'hotel_db')
        hotel_folder_path = os.path.join(os.path.dirname(__file__), 'database', 'hotel_data_new')

        if not os.path.exists(database_path):
            os.mkdir(database_path)
        else:
            return None
        self._index = create_in(database_path, self._schema)
        id = 0

        for filename in os.listdir(hotel_folder_path):
            if os.path.isfile(os.path.join(hotel_folder_path, filename)):
                print(f'Processing file: {filename}')

                with open(os.path.join(hotel_folder_path, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Open an index writer
                writer = self._index.writer()
                # Index the basic data
                basic_data = data['basic_data']
                poi_embedding = self._processor.create_and_load_hotel_embedding(basic_data.get('name', ""),
                                                                                data.get('featues', []),
                                                                                data.get('description', ""),
                                                                                data.get('reviews', []))
                #geo_info = self._geo_processor.geo_encode(basic_data.get('name', ""),
                                                          #ata['basic_data']['address']['streetAddress'] + ", "
                                                      #+ data['basic_data']['address']['addressLocality'] + ", "
                                                      #+ data['basic_data']['address']['addressCountry']['name'])

                writer.add_document(
                    id = str(id),
                    PoiType="hotel",
                    name=basic_data.get('name', None),
                    url=basic_data.get('url', None),
                    priceRange=basic_data.get('priceRange', None),
                    ratingValue=float(basic_data.get('aggregateRating', {}).get('ratingValue', 0.0)),
                    reviewCount=int(basic_data.get('aggregateRating', {}).get('reviewCount', 0)),
                    streetAddress=basic_data.get('address', {}).get('streetAddress', None),
                    addressLocality=basic_data.get('address', {}).get('addressLocality', None),
                    postalCode=basic_data.get('address', {}).get('postalCode', None),
                    addressCountry=basic_data.get('address', {}).get('addressCountry', {}).get('name', None),
                    image=basic_data.get('image', None),
                    description=data.get('description', None),
                    features=', '.join(data.get('featues', [])),
                    embedding_matrix= poi_embedding,
                    #geojson = geo_info
                )
                writer.commit()
                id = id+1

    def get_index(self):
        return self._index





