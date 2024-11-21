import yaml
from flask import Flask
from flask_cors import CORS
from core.query.query_resource import QueryResource
from core.query.query_service import QueryService
from information_retriever.information_retrival_service import InformationRetrivalService
from planner.planner_factory import LLMPlannerFactory
from planner.planning_service import PlanningService
from user_intent_processor.user_intent_service import UserIntentService
from state.state_manager import StateManager
from intelligence.singleton_llm_agent import SingletonLLMAgent
from intelligence.llm_client import LLMClient
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from query_processor.query_processing_service import QueryProcessingService
from geo_processor.geo_service import GeoService
from api_key import API_KEY, GOOGLE_API_KEY

app = Flask(__name__)
CORS(app)

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"API_KEY": API_KEY})
    config.update({"GOOGLE_API_KEY": GOOGLE_API_KEY})

#Client level
llm_client = LLMClient(SingletonLLMAgent(config).get_agent())
state_manager = StateManager()
llm_planner = LLMPlannerFactory(config).create_planner()
ask_for_recommendation = AskForRecommendation(config.get('user_intent').get('prompt'))

#Service_Level
user_intent_service = UserIntentService(llm_client, ask_for_recommendation)
ir_service = InformationRetrivalService(config.get('ir').get('prompt'), llm_client)
planning_service = PlanningService(config.get('planning').get('prompt'), llm_client)
query_processing_service = QueryProcessingService(config.get('query_processor').get('prompt'), llm_client)
geo_service = GeoService(config.get("GOOGLE_API_KEY"))
query_service = QueryService(ir_service, user_intent_service, planning_service, geo_service, query_processing_service)

#Resource Level
query_resource = QueryResource(query_service, state_manager)

# Register the blueprints
app.register_blueprint(query_resource.blueprint, url_prefix="")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
