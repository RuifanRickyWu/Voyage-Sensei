from car_travel_pipeline import CarTravel
from CarTravel.LLM.GPTChatCompletion import GPTChatCompletion
from CarTravel.config import API_KEY
import os

input_path = os.path.join(os.path.dirname(__file__), '..', 'query_process', 'queries.txt')
output_dir = os.path.join(os.path.dirname(__file__), '..', 'query_process', 'output_files', 'processed_queries.json')
llm = GPTChatCompletion(api_key=API_KEY)

instance = CarTravel(input_path, output_dir)
instance.run()