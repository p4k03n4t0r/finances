import os
import json
import openai
import time
from enum import Enum

class CATEGORY(Enum):
    GROCERIES = 1
    TRANSPORTATION = 2
    INSURANCES = 3
    UTILITIES = 4
    PETS = 5
    CLOTHES =6 
    SHOPPING =7 
    FOOD = 8
    OTHER = 9
    DONATIONS =10 
    RENT = 11
    GOVERNMENT = 12
    HEALTH = 13
    BEAUTY = 14
    UNKNOWN = 15
    SALARY = 16
    PERSONAL = 17
    ENTERTAINMENT = 18
    EDUCATION = 19
    HOUSE = 20


def enrich_with_categories():
    with open("enrich/cache.json") as cache_f:
        cache = json.load(cache_f)

    with open("enrich/personal.txt") as personal_f:
        PERSONAL = personal_f.read().split("\n")

    def decide_category_openai(party):
        while True:
            try:
                # TODO use fixed set of categories
                question = f'Which budget category does a transaction to "{party}" fall under? It\'s probably a Dutch name of a Dutch company. Only send a single word in lower case without any punctuation as answer.'
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": question}],
                )
                break
            except (
                openai.error.RateLimitError,
                openai.error.ServiceUnavailableError,
            ) as error:
                # back off due to rate limit
                print(f"openai error: {error}")
                time.sleep(20)
        answer = chat_completion.choices[0].message.content
        cache[party] = answer
        with open("enrich/cache.json",  "w") as cache_f:
            json.dump(cache, cache_f, indent=4)
        return answer
    
    def decide_category_manual(transaction):
        print(json.dumps(transaction, indent=4))
        category = CATEGORY(int(input())).name
        cache[transaction["party_clean"]] = category
        with open("enrich/cache.json",  "w") as cache_f:
            json.dump(cache, cache_f, indent=4)
        return category

    def get_category(transaction):
        party = transaction["party_clean"]
        if party in PERSONAL:
            return "PERSONAL"
        if party in cache:
            return cache[party]
        else:
            return "unknown"
            # return decide_category_manual(transaction)
            # return decide_category_openai(party)


    for file in os.listdir("output/"):
        if file.endswith(".json"):
            with open(f"output/{file}") as f:
                transactions = json.load(f)
                for transaction in transactions:
                    transaction["category"] = get_category(transaction)
            with open(f"output/{file}",  "w") as f:
                json.dump(transactions, f, indent=4)