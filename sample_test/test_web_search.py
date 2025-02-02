

import yaml
from web_search_processor.web_search_client import WebSearchClient
from api_key import OPENAI_API_KEY, GOOGLE_API_KEY

with open("../config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"OPENAI_API_KEY": OPENAI_API_KEY})
    config.update({"GOOGLE_API_KEY": GOOGLE_API_KEY})

print(config.get("web_search").get("google").get("API_KEY"))

web_search_client = WebSearchClient(config.get("web_search").get("google").get("API_KEY"),config.get("web_search").get("google").get("BASE_URL"),  config.get("web_search").get('google').get("CX"))

print(web_search_client.google_search("event for rogers center in feb 1 2025", 5))