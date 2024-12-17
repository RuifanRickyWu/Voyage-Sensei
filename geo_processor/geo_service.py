from geo_processor.google_geo_client import GoogleGeoClient
from state.state_manager import StateManager


class GeoService:
    _google_geo_client: GoogleGeoClient

    def __init__(self, google_geo_client: GoogleGeoClient):
        self._google_geo_client = google_geo_client

    def get_coords_for_plan(self, state_manager: StateManager):
        self._google_geo_client.get_coords_for_plan(state_manager)
