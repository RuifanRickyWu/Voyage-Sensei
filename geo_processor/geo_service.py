from geo_processor.google_geo_client import GoogleGeoClient
from state.state_manager import StateManager


class GeoService:
    _google_geo_client: GoogleGeoClient

    def __init__(self, google_geo_client: GoogleGeoClient):
        self._google_geo_client = google_geo_client

    def get_coords_for_plan(self, state_manager: StateManager):
        poi_list = state_manager.get_current_plan().get_poi_in_sequence()
        self._google_geo_client.get_coords_for_plan(poi_list,state_manager)
