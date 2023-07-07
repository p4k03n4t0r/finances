import os
import json
import openai
import time

with open("enrich/cache.json") as cache_f:
    cache = json.load(cache_f)


def get_category(party):
    if party in cache:
        return cache[party]
    else:
        while True:
            try:
                question = f"""Which budget category does a transaction to "{party}" fall under? 
                It's probably the name of a dutch company.
                Only send a single word in lower case without any punctuation as answer."""
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}],
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
        with open("enrich/cache.json", "w") as cache_f:
            json.dump(cache, cache_f, indent=4)
        return answer


for file in os.listdir("output/"):
    if file.endswith(".json"):
        with open(f"output/{file}") as f:
            transactions = json.load(f)
            for transaction in transactions:
                party = transaction["party"]
                transaction["category"] = get_category(party)
        with open(f"output/{file}", "w") as f:
            json.dump(transactions, f, indent=4)
