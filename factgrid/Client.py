import requests
import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from config import Configuration


class Client:

    def __init__(self, config: Configuration):
        self.config = config

    def get_results(self, query):
        try:
            logging.debug(f"Requesting FactGrid with:\n{query}")
            user_agent = "Boundary-Agents-Backend/0.2"
            sparql = SPARQLWrapper(self.config.get_fact_grid_url(), agent=user_agent)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            return 200, dict(sparql.query().convert())
        except (RuntimeError, TypeError, NameError):
            return 500, dict()
        else:
            return 503, dict()

    def get_entity_data(self, entity_id):
        url = f"{self.config.get_fact_grid_entity_data_url()}/{entity_id}.json"
        response = requests.get(url)
        return response.json()
