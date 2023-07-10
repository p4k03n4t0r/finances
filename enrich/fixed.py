import os
import json

fixed = {}

def add_transaction_to_fixed(transaction):
    month = "-".join(transaction["date"].split("-")[:2])
    if month not in fixed:
        fixed[month] = {}
    party = transaction["party"]
    if party not in fixed[month]:
        fixed[month][party] = 1
    else:
        fixed[month][party] += 1

def is_fixed(transaction):
    party = transaction["party"]
    i = 0
    # once or twice a month for at least 12 months and never three times or more
    # TODO: make it at least 6 months in a row
    for month in fixed:
        if party in fixed[month]:
            c = fixed[month][party]
            if c > 2:
                return False
            i += 1
    return i > 12


for file in os.listdir("output/"):
    if file.endswith(".json"):
        with open(f"output/{file}") as f:
            transactions = json.load(f)
            for transaction in transactions:
                add_transaction_to_fixed(transaction)

            for transaction in transactions:
                transaction["is_fixed"] = is_fixed(transaction)
        with open(f"output/{file}", "w") as f:
            json.dump(transactions, f, indent=4)