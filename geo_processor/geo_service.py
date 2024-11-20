import requests
from state.state_manager import StateManager

class GeoService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coords_from_plan(self, state_manager:StateManager):
        poi_list = state_manager.get_current_plan()
        for poi in poi_list:
            coords = self._get_location_by_address(poi['address'])
            poi['coords'] = coords
        return poi_list

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