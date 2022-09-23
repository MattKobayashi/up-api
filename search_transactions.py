#! /usr/bin/env python3
import json

accounts_file = open("accounts.json", "r")
accounts_data = json.loads(accounts_file.read())
accounts_file.close()

transactions_file = open("transactions.json", "r")
transactions_data = json.loads(transactions_file.read())
transactions_file.close()

print("\n")
print("Select the account you wish to search")
print("\n")

index = 1
for accounts in accounts_data:
    print(str(index) + ": " + str(accounts["attributes"]["displayName"]))
    index = index + 1

account_index = input("\nSelection: ")
account_index = int(account_index) - 1
account_id = accounts_data[account_index]["id"]

search_term = input("Search term: ")

matching_transactions = [
    {
        "createdAt": transaction["attributes"]["createdAt"],
        "settledAt": transaction["attributes"]["settledAt"],
        "description": transaction["attributes"]["description"],
        "message": transaction["attributes"]["message"],
        "amount": transaction["attributes"]["amount"]["value"],
        "status": transaction["attributes"]["status"],
    }
    for transaction in transactions_data
    if (
        search_term in str(transaction["attributes"]["message"])
        or search_term in str(transaction["attributes"]["description"])
    )
    and transaction["relationships"]["account"]["data"]["id"] == str(account_id)
]

print("\n")
print("--------------------")

for transaction in matching_transactions:
    print("Created at: " + transaction["createdAt"])
    if transaction["status"] == "SETTLED":
        print("Settled at: " + transaction["settledAt"])
    print("Description: " + transaction["description"])
    if transaction["message"]:
        print("Message: " + transaction["message"])
    print("Amount: " + transaction["amount"])
    print("Status: " + transaction["status"])
    print("\n")

print("Number of matches: " + str(len(matching_transactions)))
print("--------------------")
print("\n")
