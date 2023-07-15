import os
import json


def enrich_with_clean_party():
    def clean_party(party):
        party = party.upper()
        party = party.replace("CCV*","").replace("CCV","").replace("SEP*","")
        party = party.replace("B.V.","").replace("BV","").replace("B V","").replace("  "," ")
        party = party.split("VIA")[0]
        party = ''.join([i for i in party if not i.isdigit()]).strip()
        return party
    
    for file in os.listdir("output/"):
        if file.endswith(".json"):
            with open(f"output/{file}") as f:
                transactions = json.load(f)
                for transaction in transactions:
                    transaction["party_clean"] = clean_party(transaction["party"])
            with open(f"output/{file}", "w") as f:
                json.dump(transactions, f, indent=4)