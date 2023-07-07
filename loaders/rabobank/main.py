import os
import csv
import json

for file in os.listdir("input/"):
    if file.endswith(".csv"):
        transactions = []
        with open(f"input/{file}", encoding="ISO-8859-1") as f:
            reader = list(csv.reader(f, delimiter=","))
            header = reader[0]

            for line in reader[1:]:
                transaction = {}
                for i in range(len(line)):
                    transaction[header[i]] = line[i]
                if transaction["Munt"] != "EUR":
                    raise Exception(f"Unexpected currency ${transaction['Munt']}")
                transactions.append(
                    {
                        "date": transaction["Datum"],
                        "amount": float(
                            transaction["Bedrag"].replace(".", "").replace(",", ".")
                        ),
                        "party": transaction["Naam tegenpartij"],
                        "description": transaction["Omschrijving-1"],
                    }
                )

        with open(
            f"output/rabobank_{file}.json",
            "w",
            encoding="ISO-8859-1",
        ) as f:
            json.dump(transactions, f, indent=4)
