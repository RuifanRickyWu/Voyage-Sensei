import yaml
from flask import Flask
from flask_cors import CORS
from core.query.query_resource import QueryResource
from core.query.query_service import QueryService
from information_retriever.information_retrieval_service import InformationRetrievalService
from information_retriever.information_retrieval_client.llm_information_retrieval_client import LLMInformationRetrievalClient
from planner.planning_client.llm_planning_client import LLMPlanningClient
from planner.planning_service import PlanningService
from user_intent_processor.user_intent_service import UserIntentService
from user_intent_processor.user_intent_client import UserIntentClient
from state.state_manager import StateManager
from intelligence.llm_agent import LLMAgent
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from geo_processor.google_geo_client import GoogleGeoClient
from api_key import OPENAI_API_KEY, GOOGLE_API_KEY

app = Flask(__name__)
CORS(app)

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"OPENAI_API_KEY": OPENAI_API_KEY})
    config.update({"GOOGLE_API_KEY": GOOGLE_API_KEY})

state_manager = StateManager()

#Client level
llm_agent = LLMAgent(config, "GPT")
ask_for_recommendation = AskForRecommendation(config.get('user_intent').get('prompt'))
user_intent_client = UserIntentClient(llm_agent, ask_for_recommendation)
llm_information_retrieval_client = LLMInformationRetrievalClient(llm_agent, config.get('ir').get('prompt'))
llm_planning_client = LLMPlanningClient(llm_agent, config.get('planning').get('prompt'))
google_geo_client = GoogleGeoClient(config.get("GOOGLE_API_KEY"), config.get("geo_processor").get("google").get("BASE_URL"))


#Service_Level
user_intent_service = UserIntentService(user_intent_client, ask_for_recommendation)
ir_service = InformationRetrievalService(llm_information_retrieval_client)
planning_service = PlanningService(llm_planning_client)
query_processing_service = QueryProcessingService(config.get('query_processor').get('prompt'), llm_agent)
geo_service = GeoService(config.get("GOOGLE_API_KEY"))
query_service = QueryService(ir_service, user_intent_service, planning_service, geo_service, query_processing_service)

#Resource Level
query_resource = QueryResource(query_service, state_manager)

# Register the blueprints
app.register_blueprint(query_resource.blueprint, url_prefix="")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
