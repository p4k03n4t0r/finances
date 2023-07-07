from elasticsearch import Elasticsearch
import os
import json

es = Elasticsearch("http://localhost:9200")

# TODO create expenses index with date as timestamp field and id as id

for file in os.listdir("output/"):
    if file.endswith(".json"):
        with open(f"output/{file}") as f:
            transactions = json.load(f)
            for transaction in transactions:
                es.index(index="expenses", document=transaction)
