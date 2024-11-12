from system.base_system import BASE_SYSTEM
from information_retriever.search_engine.search_engine import SearchEngine


class BaseLine(BASE_SYSTEM):
    _config_path: str

    def __init__(self, config_path: str):
        self._config_path = config_path


    def run(self):

        pass