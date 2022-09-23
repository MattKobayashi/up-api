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
    if os.path.exists("accounts.json"):
        update_accounts_file()
        print("Accounts file updated successfully!")
    else:
        print("No existing accounts data file found, creating a new one...")
        update_accounts_file()
        print("Accounts file created successfully!")


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


def update_accounts_file():

    # Set the API URL for accounts
    up_api_accounts_url = "https://api.up.com.au/api/v1/accounts?page[size]=100"

    # Grab the first page of accounts
    up_api_data_response = requests.get(
        up_api_accounts_url, headers=up_api_token
    ).json()
    transaction_data = up_api_data_response["data"]

    # Iterate if there's more than one page (of course there will be)
    while up_api_data_response["links"]["next"]:
        up_api_data_response = requests.get(
            up_api_data_response["links"]["next"], headers=up_api_token
        ).json()
        transaction_data.extend(up_api_data_response["data"])

    # Write the accounts data to the file
    accounts_file = open("accounts.json", "w")
    accounts_file.write(json.dumps(transaction_data))
    accounts_file.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        exit()
