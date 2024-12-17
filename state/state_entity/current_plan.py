from state.state_entity.POI import POI


class CurrentPlan:
    _sequence: list[str]
    _POI_in_sequence: list[POI]
    _summary: str

    def __init__(self, POI_in_sequence: list[POI] = None, summary: str = None):
        self._POI_in_sequence = POI_in_sequence
        self._summary = summary

    def update_summary(self, summary: str):
        self._summary = summary

    def update_poi_in_sequence(self, POI_in_sequence: list[POI]):
        self._POI_in_sequence = POI_in_sequence

    def get_summary(self):
        return self._summary

    def get_poi_in_sequence(self):
        return self._POI_in_sequence

    def get_converted_planned_poi_list(self):
        poi_list = []
        for poi in self._POI_in_sequence:
            poi_list.append(poi.get_poi())
        return poi_list

    def form_current_plan(self):
        itinerary = {}
        itinerary["summary"] = self._summary
        poi_in_sequence = []
        for poi in self._POI_in_sequence:
            poi_in_sequence.append(poi.get_poi(["name", "coords", "keywords"]))
        itinerary["poi_sequence"] = poi_in_sequence

        return itinerary



