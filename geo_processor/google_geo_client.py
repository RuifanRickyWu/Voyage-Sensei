from state.state_manager import StateManager
import requests

class GoogleGeoClient:

    _api_key: str
    _base_url = str

    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url

    def get_coords_for_plan(self, state_manager:StateManager):
        poi_list = state_manager.get_current_plan().get_POI_in_sequence()
        for poi in poi_list:
            coords = self._get_location_by_address(poi.get_poi().get("address"))
            poi.update_coordinates(coords)

    def _get_location_by_address(self, address):
        params = {
            'address': address,
            'key': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                raise ValueError(f"Address not found: {address}")
        else:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")



