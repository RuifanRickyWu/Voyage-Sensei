from state.state_entity.POI import POI


class Itinerary:
    _sequence: list[str]
    _summary: str
    _itinerary_detail: list[POI]

    def __init__(self):
        self._sequence = []

    def update_sequence(self, sequence: list[str]):
        self._sequence = sequence

    def update_summary(self, summary: str):
        self._summary = summary

    def update_full_trip_detail(self, itinerary_detail: list[POI]):
        self._itinerary_detail = itinerary_detail

    def get_sequence(self):
        return self._sequence

    def get_summary(self):
        return self._summary

    def get_itinerary(self):
        full_list = []
        for poi in self._itinerary_detail:
            full_list.append(poi.get_poi())
        return full_list
