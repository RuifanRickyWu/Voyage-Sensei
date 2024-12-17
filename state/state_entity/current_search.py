from state.state_entity.POI import POI


class CurrentSearch:

    _retrieved_poi_list: list[POI]

    def __init__(self, retrieved_poi_list: list[POI] = None):
        self._retrieved_poi_list = retrieved_poi_list

    def update_retrieved_poi_list(self, retrieved_poi_list: list[POI]):
        self._retrieved_poi_list = retrieved_poi_list

    def get_retrieved_poi_list(self):
        return self._retrieved_poi_list

    def get_converted_retrieved_poi_list(self):
        poi_list = []
        for poi in self._retrieved_poi_list:
            poi_list.append(poi.get_poi())
        return poi_list

