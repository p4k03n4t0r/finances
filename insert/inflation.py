from elasticsearch import Elasticsearch
import os
import csv
import requests

def import_inflation():
    es_url = "http://localhost:9200"
    index_name = "inflation"
    requests.delete(f"{es_url}/{index_name}")
    es = Elasticsearch(es_url)
    # TODO set id as _id?

    def to_date(year, dutch_month):
        dutch_month = dutch_month.replace("*", "")
        if dutch_month == "januari":
            month = "01"
        elif dutch_month == "februari":
            month = "02"
        elif dutch_month == "maart":
            month = "03"
        elif dutch_month == "april":
            month = "04"
        elif dutch_month == "mei":
            month = "05"
        elif dutch_month == "juni":
            month = "06"
        elif dutch_month == "juli":
            month = "07"
        elif dutch_month == "augustus":
            month = "08"
        elif dutch_month == "september":
            month = "09"
        elif dutch_month == "oktober":
            month = "10"
        elif dutch_month == "november":
            month = "11"
        elif dutch_month == "december":
            month = "12"
        else:
            raise Exception(f"Unkown Dutch month {dutch_month}")
        return f"{year}-{month}-01"


    inflation = []
    for file in os.listdir("output/"):
        if file.endswith(".csv"):
            with open(f"output/{file}", encoding="ISO-8859-1") as f:
                reader = list(csv.reader(f, delimiter=";"))
                header = reader[0]
                for line in reader[1:]:
                    parsed_line = {}
                    for i in range(len(line)):
                        parsed_line[header[i]] = line[i]
                    change = float(parsed_line["CPI"].replace(",", "."))
                    inflation.append(
                        {
                            "date": to_date(parsed_line["Jaar"], parsed_line["Maand"]),
                            "change": change,
                        }
                    )


    for month in inflation:
        es.index(index=index_name, id=month["date"], document=month)
