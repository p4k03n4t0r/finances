from elasticsearch import Elasticsearch
import os
import json
import requests

def import_expenses():
    es_url = "http://localhost:9200"
    index_name = "expenses"
    requests.delete(f"{es_url}/{index_name}")
    es = Elasticsearch(es_url)

    for file in os.listdir("output/"):
        if file.endswith(".json"):
            with open(f"output/{file}") as f:
                transactions = json.load(f)
                for transaction in transactions:
                    es.index(index=index_name, id=transaction["id"], document=transaction)
