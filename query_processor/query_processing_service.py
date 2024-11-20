import json, os, re, pickle
from tqdm import tqdm

from state.query import Query
from jinja2 import Environment, FileSystemLoader
from intelligence.llm_client import LLMClient

class QueryProcessingService:

    def __init__(self, prompt_config: dict, llm_client: LLMClient):
        """
        Initialize the query processor
        :param query:
        :param llm:
        :param mode_name: can only be "expand", "reformulate", "elaborate"
        :param output_dir:
        """ 
        # self.llm = llm
        self.query_list = []
        self.results = None
        self._prompt_config = prompt_config
        self._llm_client = llm_client
    
    def load_query(self, query: str) -> list[Query]:
        query = query.lower()
        query = Query(query)
        self.query_list.append(query)
    
    def process_queries(self) -> list[Query]:
        """
        Q2E: get all aspects from list of queries
        """
        query = ''
        for q in self.query_list:
            query += q.description
            query += '\n'
        self.results = self.extract_aspects(query)
        
        return self.results

    def get_results(self):
        return self.results
    
    def _load_prompt_zeroshot(self, query):
        env = Environment(loader=FileSystemLoader(self._prompt_config.get("PROMPT_PATH")))
        # print("printing zeroshot_apsect_extraction...")
        # print(self._prompt_config.get("ZEROSHOT_ASPECT_EXTRACTION"))
        template = env.get_template(self._prompt_config.get("ZEROSHOT_ASPECT_EXTRACTION"))
        message = template.render(user_query=query)
        print(message)
        return message
    
    def extract_aspects(self, query: str) -> tuple[list[str], list[str], list[str]]:
        """
        Extract aspects/entities from the query string
        """
        message = self._load_prompt_zeroshot(query)
        result = json.loads(self._llm_client.make_request(message))
        return result