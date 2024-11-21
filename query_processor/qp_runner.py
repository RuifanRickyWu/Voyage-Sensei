import os

import sys
sys.path.append('/Users/yikaimaa/Desktop/capstone_dev/Voyage-Sensei')

import json
from intelligence.llm_client import LLMClient
from state.query import Query
from core.query.query_resource import QueryResource
from core.query.query_service import QueryService
from intelligence.singleton_llm_agent import SingletonLLMAgent

from query_processor.query_processing_service import QueryProcessingService
from api_key import API_KEY
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"API_KEY": API_KEY})
    
# #Client level
# llm_client = LLMClient(SingletonLLMAgent(config).get_agent())
# state_manager = StateManager()
# llm_planner = LLMPlannerFactory(config).create_planner()
# ask_for_recommendation = AskForRecommendation(config.get('user_intent').get('prompt'))

# #Service_Level
# user_intent_service = UserIntentService(llm_client, ask_for_recommendation)
# ir_service = InformationRetrivalService(config.get('ir').get('prompt'), llm_client)
# planning_service = PlanningService(config.get('planning').get('prompt'), llm_client)
# query_processing_service = QueryProcessingService(config.get('query_processor').get('prompt'), llm_client)
# query_service = QueryService(ir_service, user_intent_service, planning_service, query_processing_service)

# #Resource Level
# query_resource = QueryResource(query_service, state_manager)

def test_query_processing_service():
    # Load mock configuration for the query processor (replace with your actual configuration)
    prompt_config = {
        "PROMPT_PATH": "prompt_files/query_processor",  # path to the prompt templates directory
        "ZEROSHOT_ASPECT_EXTRACTION": "zeroshot_aspect_extraction.jinja",  # the name of the prompt template file
    }

    # Create a mock LLM client (replace with actual client or mock if necessary)
    llm_client = LLMClient(SingletonLLMAgent(config).get_agent())
    
    # Create an instance of the QueryProcessingService
    query_processor = QueryProcessingService(prompt_config=prompt_config, llm_client=llm_client)

    # Test data: add sample queries (replace these with actual `Query` objects as needed)
    query1 = "Where can I find a good Italian restaurant near me?"
    query2 = "What are the best tourist attractions in Paris?"
    
    query_processor.load_query(query1)
    query_processor.load_query(query2)
    
    # Process the queries and retrieve the results
    results = query_processor.process_queries()
    
    # Print the results (replace with your desired assertion or further processing)
    print("Processed Results:")
    print(results)
    
    # Assuming you have a `get_results` function to return processed results:
    processed_results = query_processor.get_results()
    print("\nFinal Processed Results:")
    print(processed_results)

if __name__ == "__main__":
    test_query_processing_service()
