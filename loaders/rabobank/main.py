import os
import csv
import json

def load_rabobank():
    transactions = []
    for file in os.listdir("input/"):
        if file.endswith(".csv"):
            with open(f"input/{file}", encoding="ISO-8859-1") as f:
                reader = list(csv.reader(f, delimiter=","))
                header = reader[0]

                for line in reader[1:]:
                    transaction = {}
                    for i in range(len(line)):
                        transaction[header[i]] = line[i]
                    if transaction["Munt"] != "EUR":
                        raise Exception(f"Unexpected currency {transaction['Munt']}")
                    amount = transaction["Bedrag"].replace(".", "").replace(",", ".")
                    amount_sign = amount[0]
                    amount = amount[1:]
                    transactions.append(
                        {
                            "id": transaction["Transactiereferentie"],
                            "date": transaction["Datum"],
                            "amount": float(amount),
                            "net_amount": float(amount_sign + amount),
                            "credit_or_debit": amount_sign,
                            "party": transaction["Naam tegenpartij"],
                            "description": transaction["Omschrijving-1"],
                            "account_balance": float(transaction["Saldo na trn"].replace("+","").replace(",",".")),
                            "bank": "Rabobank",
                        }
                    )

    with open(
        f"output/rabobank.json",
        "w",
    ) as f:
        json.dump(transactions, f, indent=4)
