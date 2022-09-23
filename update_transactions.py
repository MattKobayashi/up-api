#! /usr/bin/env python3
import requests
import json
import os

up_api_ping_url = "https://api.up.com.au/api/v1/util/ping"
up_api_token = {"Authorization": "Bearer " + os.environ.get("UP_API_TOKEN")}


def main():
    try:
        ping_up_api()
    except Exception:
        exit()
    if os.path.exists("transactions.json") and os.path.getsize("transactions.json") > 0:
        print("Existing transactions data file found, attempting to update it...")
        update_transactions_file()
    elif os.path.getsize("transactions.json") == 0:
        print("Transactions data file is empty, re-populating...")
        create_transactions_file()
    else:
        print("No existing transactions data file found, creating a new one...")
        create_transactions_file()


def ping_up_api():
    up_api_ping_response = requests.get(up_api_ping_url, headers=up_api_token)

    if up_api_ping_response.status_code == 200:
        print("API query successful, retrieving data...")
        return
    else:
        print(
            "API query unsuccessful, response code was "
            + str(up_api_ping_response.status_code)
        )
        raise Exception()


def create_transactions_file():

    # Set the API URL for transactions
    up_api_transactions_url = "https://api.up.com.au/api/v1/transactions?page[size]=100"

    # Grab the first page of transactions
    up_api_data_response = requests.get(
        up_api_transactions_url, headers=up_api_token
    ).json()
    transactions_data = up_api_data_response["data"]

    # Iterate if there's more than one page (of course there will be)
    while up_api_data_response["links"]["next"]:
        up_api_data_response = requests.get(
            up_api_data_response["links"]["next"], headers=up_api_token
        ).json()
        transactions_data.extend(up_api_data_response["data"])

    # Write the transaction data to the file
    transactions_file = open("transactions.json", "w")
    transactions_file.write(json.dumps(transactions_data))
    transactions_file.close()

    # It worked!
    print("Transactions data file created successfully!")


def update_transactions_file():
    transactions_file = open("transactions.json", "r")
    existing_transactions_data = json.loads(transactions_file.read())
    transactions_file.close()

    # Set the API URL for new transactions
    up_api_transactions_url = (
        "https://api.up.com.au/api/v1/transactions?page[size]=100&filter[since]="
        + str(existing_transactions_data[0]["attributes"]["createdAt"]).replace(
            "+", "%2B"
        )
    )

    # Grab the first page of new transactions
    up_api_data_response = requests.get(
        up_api_transactions_url, headers=up_api_token
    ).json()
    new_transactions_data = up_api_data_response["data"]

    # Iterate if there's more than one page returned by the API
    while up_api_data_response["links"]["next"]:
        up_api_data_response = requests.get(
            up_api_data_response["links"]["next"], headers=up_api_token
        ).json()
        new_transactions_data.extend(up_api_data_response["data"])

    # Merge data and deduplicate
    combined_transactions_data = list(
        {
            transaction["id"]: transaction
            for transaction in existing_transactions_data + new_transactions_data
        }.values()
    )

    # Check to see if there's actually any new data
    if len(combined_transactions_data) == len(existing_transactions_data):
        print("No new data available!")
        exit()

    # Write the combined transaction data to the file
    transactions_file = open("transactions.json", "w")
    transactions_file.write(json.dumps(combined_transactions_data))
    transactions_file.close()

    # It worked!
    print("Transactions data updated successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit()
