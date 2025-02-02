from datetime import date

import requests


class WebSearchClient:
    _api_key: str
    #search engine id
    _cx: str
    _base_url: str

    def __init__(self, api_key: str, base_url:str, cx: str):
        self._cx = cx
        self._base_url = base_url
        self._api_key = api_key

    def google_search(self, query:str, n_result:int):
        params = {
            "q": query,
            "key": self._api_key,
            "cx": self._cx,
            "num": n_result
        }
        response = requests.get(self._base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("failed to search:", response.json())
            return None