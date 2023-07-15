import os
import json

def enrich_with_fixed():
    with open("enrich/fixed.txt") as f:
        fixed_list = f.read().split("\n") 


    def is_fixed(transaction):
        return "fixed" if transaction["party"] in fixed_list else "flexible"


    for file in os.listdir("output/"):
        if file.endswith(".json"):
            with open(f"output/{file}") as f:
                transactions = json.load(f)
                for transaction in transactions:
                    transaction["is_fixed"] = is_fixed(transaction)
            with open(f"output/{file}", "w") as f:
                json.dump(transactions, f, indent=4)
