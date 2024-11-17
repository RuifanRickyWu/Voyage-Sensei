import yaml
from flask import Flask
from flask_cors import CORS
from core.query.query_resource import QueryResource
from core.query.query_service import QueryService
from information_retriever.information_retriever_factory import LLMBasedIRFactory
from planner.planner_factory import LLMPlannerFactory
from user_intent_processor.user_intent_service import UserIntentService
from state.state_manager import StateManager
from intelligence.singleton_llm_agent import SingletonLLMAgent
from user_intent_processor.user_intent.ask_for_recommendation import AskForRecommendation
from api_key import API_KEY

app = Flask(__name__)
CORS(app)

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config.update({"API_KEY": API_KEY})

llm_agent = SingletonLLMAgent(config).get_agent()
state_manager = StateManager()
llm_search_engine = LLMBasedIRFactory(config).create_search_engine()
llm_planner = LLMPlannerFactory(config).create_planner()
ask_for_recommendation = AskForRecommendation(config.get('user_intent').get('prompt'))

user_intent_service = UserIntentService(llm_agent, ask_for_recommendation)
query_service = QueryService(llm_search_engine, user_intent_service, llm_planner)
query_resource = QueryResource(query_service, state_manager)

# Register the blueprints
app.register_blueprint(query_resource.blueprint, url_prefix="")

if __name__ == "__main__":
    app.run(port=5000, debug=True)