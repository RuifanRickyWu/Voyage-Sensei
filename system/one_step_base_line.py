import yaml

from system.base_system import BASE_SYSTEM
from planner.planner_factory import OneStepLLMPlannerFactory
from api_key import API_KEY


class OneStepBaseLine(BASE_SYSTEM):
    _config: dict

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)
            self._config.update({"API_KEY": API_KEY})

    def run(self):
        planner_factory = OneStepLLMPlannerFactory(self._config)
        planner = planner_factory.create_planner()
        query = "jazz based theme"
        poi_sequence = planner.plan(query)
        print(poi_sequence)

