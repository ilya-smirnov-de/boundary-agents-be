from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS
from waitress import serve

import constants
from config import Configuration
import logging
import os
import threading
from factgrid.Queries import Queries as FactGridQueries
from factgrid.Client import Client as FactGridClient
from factgrid.Downloader import Downloader as FactGridDownloader

loglevel = logging.DEBUG
if os.environ.get("DEBUG") is not None and (os.environ["DEBUG"] == "1" or os.environ["DEBUG"].upper() == "TRUE"):
    loglevel = logging.DEBUG

config = Configuration()
logging.root.setLevel(loglevel)
logging.basicConfig(encoding='utf-8', level=loglevel)

app = Flask(__name__)
CORS(app)
fg_client = FactGridClient(config)
queries = FactGridQueries()


def get_lang(args):
    if args.get('lang') is not None and len(args.get('lang')):
        lang = args.get('lang').lower()
        if lang in constants.LANGUAGES:
            return lang
    return constants.DEFAULT_LANG


@app.route("/agents/<agent_id>", methods=['GET'])
def get_agent(agent_id):
    res = fg_client.get_results(queries.get_agent(agent_id=agent_id, lang=get_lang(request.args)))
    return res[1]["results"]["bindings"][0]


@app.route("/agents/<agent_id>/geo/<property_id>", methods=['GET'])
def get_agent_geo_property(agent_id, property_id):
    if property_id in constants.PROPERTY_TYPES:
        property_id = constants.PROPERTY_TYPES[property_id]
    res = fg_client.get_results(queries.get_geo_property(agent_id=agent_id, property_id=property_id, lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]


@app.route("/agents/<agent_id>/listproperty/<property_id>", methods=['GET'])
def get_list(agent_id, property_id):
    if property_id in constants.PROPERTY_TYPES:
        property_id = constants.PROPERTY_TYPES[property_id]
    res = fg_client.get_results(queries.get_list(agent_id=agent_id, property_id=property_id, lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]


@app.route("/agents/<agent_id>/relations/<relation_id>", methods=['GET'])
def get_agent_relation(agent_id, relation_id):
    if relation_id in constants.RELATION_TYPES:
        relation_id = constants.RELATION_TYPES[relation_id]
    res = fg_client.get_results(queries.get_relations(agent_id=agent_id, relation_id=relation_id, lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]


@app.route("/entity/<entity_id>", methods=['GET'])
def get_entity_data(entity_id):
    res = fg_client.get_entity_data(entity_id=entity_id)
    return res


@app.route("/courts", methods=['GET'])
def get_courts():
    res = fg_client.get_results(queries.get_courts(lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]

@app.route("/courts/<court_id>", methods=['GET'])
def get_court_details(court_id):
    res = fg_client.get_results(queries.get_court_details(court_id=court_id, lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]

@app.route("/agents", methods=['GET'])
def get_agents_list():
    keyword, birth_from, birth_to = "","",""
    if request.args is not None:
        logging.debug("Request args: ")
        logging.debug(vars(request.args))
        if request.args.get('keyword') is not None:
            keyword = request.args.get('keyword').strip()
        if request.args.get('birthFrom') is not None:
            birth_from = str(request.args.get('birthFrom')).strip()
        if request.args.get('birthTo') is not None:
            birth_to = str(request.args.get('birthTo')).strip()

    res = fg_client.get_results(queries.get_agents(keyword=keyword,
                                                   birth_from=birth_from,
                                                   birth_to=birth_to,
                                                   lang=get_lang(request.args)))
    return res[1]["results"]["bindings"]


@app.route("/recache", methods=['GET'])
def get_recache():
    t = threading.Thread(target=download_cache, args=[])
    t.start()
    return Response(status=200)


def download_cache():
    dl = FactGridDownloader(client=fg_client)
    dl.download_entities()


if __name__ == "__main__":
    serve(app, host="localhost", port=config.get_port())
