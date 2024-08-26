from CarTravel.data_process.whoosh_database import WhooshDB

class DB_Service:
    _whooshDB: WhooshDB

    def __init__(self):
        self._whooshDB = WhooshDB()

    def create_db(self):
        self._whooshDB.create_and_load_hotel_index()

    def filter_search(self, constraints: list[str]):
        return self._whooshDB.query(constraints)



