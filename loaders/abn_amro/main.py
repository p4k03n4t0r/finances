import os
from zipfile import ZipFile
import xmltodict
import json

def load_abn_amro():
    for file in os.listdir("input/"):
        if file.endswith(".zip"):
            with ZipFile(f"input/{file}", "r") as f:
                f.extractall("input/")

    with open("loaders/accounts.txt") as f:
        ACCOUNTS = f.read().split("\n")

    transactions = []
    def get_account_balance(transactions_for_date):
        return float(
                        transactions_for_date["Document"]["BkToCstmrStmt"]["Stmt"]["Bal"][
                            1
                        ]["Amt"]["#text"]
                    )

    def get_id(entry):
        if "AcctSvcrRef" in entry:
            id = entry["AcctSvcrRef"]
        else:
            id = hash(entry["AddtlNtryInf"])
        return id

    def get_party(entry):
        if "NtryDtls" in entry:
            if entry["CdtDbtInd"] == "DBIT":
                party = entry["NtryDtls"]["TxDtls"]["RltdPties"]["Cdtr"]["Nm"]
            else:
                party = entry["NtryDtls"]["TxDtls"]["RltdPties"]["Dbtr"]["Nm"]
        else:
            party = entry["AddtlNtryInf"][32:].split(",PAS064")[0]
        return party

    def check_currency_is_euro(entry):
        if entry["Amt"]["@Ccy"] != "EUR":
            raise Exception(f"Unexpected currency {entry['Amt']['@Ccy']}")

    def get_description(entry):
        if (
                        "NtryDtls" in entry
                        and "RmtInf" in entry["NtryDtls"]["TxDtls"]
                        and "Ustrd" in entry["NtryDtls"]["TxDtls"]["RmtInf"]
                    ):
            description = entry["NtryDtls"]["TxDtls"]["RmtInf"]["Ustrd"]
        else:
            description = entry["AddtlNtryInf"]
        return description

    def get_is_savings(entry):
        if "NtryDtls" not in entry:
            return False
        if "CdtrAcct" in entry["NtryDtls"]["TxDtls"]["RltdPties"]:
            account =  entry["NtryDtls"]["TxDtls"]["RltdPties"]["CdtrAcct"]["Id"]["IBAN"]
        elif "DbtrAcct" in entry["NtryDtls"]["TxDtls"]["RltdPties"]:
            account =  entry["NtryDtls"]["TxDtls"]["RltdPties"]["DbtrAcct"]["Id"]["IBAN"]
        else:
            return False
        return account in ACCOUNTS

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
                    check_currency_is_euro(entry)
                    amount_sign = "-" if entry["CdtDbtInd"] == "DBIT" else "+"
                    party = get_party(entry)
                    description = get_description(entry)
                    id = get_id(entry)
                    account_balance = get_account_balance(transactions_for_date)
                    is_savings = get_is_savings(entry)
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
                            "is_savings": is_savings
                        }
                    )

    with open(f"output/abn_amro.json", "w") as f:
        json.dump(transactions, f, indent=4)
