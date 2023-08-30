import urllib.request
import os
from time import sleep
from factgrid import Client as FactGridClient
from factgrid import Queries as FactGridQueries


class Downloader:

    def __init__(self, client: FactGridClient):
        self.client = client

    def download_entities(self):
        for file_name in os.listdir("./cache"):
            file = "./cache/" + file_name
            if os.path.isfile(file):
                os.remove(file)
        q = FactGridQueries()
        res = self.client.get_results(q.get_project_items())
        count = 0
        for item in res["results"]["bindings"]:
            q_id = item["item"]["value"]
            entry_id = q_id.split('/')[-1]
            addr = f"https://database.factgrid.de/wiki/Special:EntityData/{entry_id}.json"
            try:
                urllib.request.urlretrieve(addr, "cache/" + entry_id + ".json")
            except:
                print("Error")
            else:
                count += 1
                sleep(30)
        print(f"Downloaded {count} files")
