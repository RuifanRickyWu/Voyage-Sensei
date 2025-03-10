import logging

import yaml
from flask import Flask
from flask_cors import CORS
from core.query.query_resource import QueryResource
from core.query.query_service import QueryService
from core.critique.critique_service import CritiqueService
from core.critique.critique_resource import CritiqueResource
from core.critique.critique_client.critique_client import CritiqueClient
from information_retriever.information_retrieval_service import InformationRetrievalService
from information_retriever.information_retrieval_client.llm_information_retrieval_client import \
    LLMInformationRetrievalClient
from planner.planning_client.llm_planning_client import LLMPlanningClient
from planner.planning_service import PlanningService
from user_intent_processor.user_intent_service import UserIntentService
from user_intent_processor.user_intent_client import UserIntentClient
from state.state_manager import StateManager
from intelligence.llm_agent import LLMAgent
from web_search_processor.web_search_client import WebSearchClient
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from user_intent_processor.user_intent.provide_preference import ProvidePreference
from user_intent_processor.user_intent.cut_off_input import CutOffInput
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from geo_processor.google_geo_client import GoogleGeoClient
from reasoner.reasoning_service import ReasoningService
from reasoner.reasoning_client import ReasoningClient
from api_key import OPENAI_API_KEY, GOOGLE_API_KEY
from event_processor.event_processor_service import EventProcessorService
from event_processor.event_processor_client import EventProcessorClient


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log", mode="w")
        ]
    )


setup_logger()

app = Flask(__name__)
CORS(app)

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"OPENAI_API_KEY": OPENAI_API_KEY})
    config.update({"GOOGLE_API_KEY": GOOGLE_API_KEY})

state_manager = StateManager()

#Client level
llm_agent = LLMAgent(config, "GPT")
critique_client = CritiqueClient(llm_agent, config.get('critique').get('prompt'))
web_search_client = WebSearchClient(config.get("web_search").get("google").get("API_KEY"),
                                    config.get("web_search").get("google").get("BASE_URL"),
                                    config.get("web_search").get('google').get("CX"))
event_processor_client = EventProcessorClient(llm_agent, web_search_client, config.get('event_processor').get('prompt'))
ask_for_recommendation = AskForRecommendation(config.get('user_intent').get('prompt'))
provide_preference = ProvidePreference(config.get('user_intent').get('prompt'))
cut_off_input = CutOffInput(config.get('user_intent').get('prompt'))
user_intent_client = UserIntentClient(llm_agent, ask_for_recommendation, provide_preference, cut_off_input)
llm_information_retrieval_client = LLMInformationRetrievalClient(llm_agent, config.get('ir').get('prompt'))
llm_planning_client = LLMPlanningClient(llm_agent, config.get('planning').get('prompt'))
google_geo_client = GoogleGeoClient(config.get("GOOGLE_API_KEY"),
                                    config.get("geo_processor").get("google").get("BASE_URL"))
reasoning_client = ReasoningClient(llm_agent, config.get('reasoner').get('prompt'))

#Service_Level
event_processor_service = EventProcessorService(event_processor_client)
user_intent_service = UserIntentService(user_intent_client, ask_for_recommendation)
ir_service = InformationRetrievalService(llm_information_retrieval_client)
planning_service = PlanningService(llm_planning_client)
query_processing_service = QueryProcessingService(config.get('query_processor').get('prompt'), llm_agent)
geo_service = GeoService(google_geo_client)
reasoning_service = ReasoningService(reasoning_client)
query_service = QueryService(ir_service, user_intent_service, planning_service, geo_service, query_processing_service,
                             reasoning_service, event_processor_service)
critique_service = CritiqueService(ir_service, user_intent_service, planning_service, geo_service, query_processing_service, reasoning_service, event_processor_service, critique_client)

#Resource Level
query_resource = QueryResource(query_service, state_manager)
critique_resource = CritiqueResource(critique_service, state_manager)

# Register the blueprints
app.register_blueprint(query_resource.blueprint, url_prefix="")
app.register_blueprint(critique_resource.blueprint, url_prefix="")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
