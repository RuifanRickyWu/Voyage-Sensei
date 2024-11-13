import yaml

from system.base_system import BASE_SYSTEM
from information_retriever.information_retriever_factory import LLMBasedIRFactory
from planner.planner_factory import LLMPlannerFactory
from api_key import API_KEY


class BaseLine(BASE_SYSTEM):
    _config: dict

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)
            self._config.update({"API_KEY": API_KEY})

    def run(self):
        ir_factory = LLMBasedIRFactory(self._config)
        planner_factory = LLMPlannerFactory(self._config)
        search_engine = ir_factory.create_search_engine()
        planner = planner_factory.create_planner()


        query = "jazz based theme"
        print(query)
        print(search_engine.get_topk_poi(query))
