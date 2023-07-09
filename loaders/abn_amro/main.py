import os
from zipfile import ZipFile
import xmltodict
import json

for file in os.listdir("input/"):
    if file.endswith(".zip"):
        with ZipFile(f"input/{file}", "r") as f:
            f.extractall("input/")

transactions = []
for file in os.listdir("input/"):
    if file.endswith(".xml"):
        with open(f"input/{file}") as f:
            transactions_for_date = xmltodict.parse(f.read())
            entries = transactions_for_date["Document"]["BkToCstmrStmt"]["Stmt"]["Ntry"]
            # If there is a single entry, the XML parser doesn't make it a list
            # so this 'hack' ensures it's a list
            if "Amt" in entries:
                entries = [entries]
            for entry in entries:
                if entry["Amt"]["@Ccy"] != "EUR":
                    raise Exception(f"Unexpected currency {entry['Amt']['@Ccy']}")
                amount_sign = "-" if entry["CdtDbtInd"] == "DBIT" else "+"
                if "NtryDtls" in entry:
                    if entry["CdtDbtInd"] == "DBIT":
                        party = entry["NtryDtls"]["TxDtls"]["RltdPties"]["Cdtr"]["Nm"]
                    else:
                        party = entry["NtryDtls"]["TxDtls"]["RltdPties"]["Dbtr"]["Nm"]
                else:
                    party = entry["AddtlNtryInf"][32:].split(",PAS064")[0]
                if (
                    "NtryDtls" in entry
                    and "RmtInf" in entry["NtryDtls"]["TxDtls"]
                    and "Ustrd" in entry["NtryDtls"]["TxDtls"]["RmtInf"]
                ):
                    description = entry["NtryDtls"]["TxDtls"]["RmtInf"]["Ustrd"]
                else:
                    description = entry["AddtlNtryInf"]
                if "AcctSvcrRef" in entry:
                    id = entry["AcctSvcrRef"]
                else:
                    id = hash(entry["AddtlNtryInf"])
                account_balance = float(
                    transactions_for_date["Document"]["BkToCstmrStmt"]["Stmt"]["Bal"][
                        1
                    ]["Amt"]["#text"]
                )
                transactions.append(
                    {
                        "id": id,
                        "date": entry["BookgDt"]["Dt"],
                        "amount": float(entry["Amt"]["#text"]),
                        "net_amount": float(amount_sign + entry["Amt"]["#text"]),
                        "credit_or_debit": amount_sign,
                        "party": party,
                        "description": description,
                        "account_balance": account_balance,
                        "bank": "ABN_AMRO",
                    }
                )

with open(f"output/abn_amro.json", "w") as f:
    json.dump(transactions, f, indent=4)
