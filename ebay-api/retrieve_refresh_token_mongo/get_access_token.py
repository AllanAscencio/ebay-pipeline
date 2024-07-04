import pymongo
import functools
import base64
import json
import requests
import sys
from urllib.parse import unquote


PATH_TO_CREDS = "config.json"

@functools.lru_cache(maxsize=1)
def get_mongo_client():
    return pymongo.MongoClient(
        "mongodb+srv://myUser:myPassword@cluster0.mongodb.net/myDatabase?retryWrites=true&w=majority"
    )   


@functools.lru_cache(maxsize=1)
def get_ebay_database():
    client = get_mongo_client()
    return client["ebay_database"]


@functools.lru_cache(maxsize=1)
def get_user_access_table():
    db = get_ebay_database()
    return db["user_access_tokens"]


@functools.lru_cache(maxsize=1)
def get_user_refresh_token(username):
    table = get_user_access_table()
    user_record = table.find_one({"userName": username})
    if not user_record:
        print("User not found")
        return
    return user_record["refreshToken"]


@functools.lru_cache(maxsize=1)
def load_credentials(config_path=PATH_TO_CREDS):
    with open(config_path, "r") as file:
        return json.load(file)


@functools.lru_cache(maxsize=1)
def encode_credentials(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}".encode()
    return base64.b64encode(credentials).decode()


@functools.lru_cache(maxsize=1)
def construct_headers(encoded_credentials):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + encoded_credentials,
    }


def exchange_refresh_token_for_access_token(encoded_credentials, refresh_token):
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = construct_headers(encoded_credentials)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


def get_access_token(username):
    creds = load_credentials()
    encoded_credentials = encode_credentials(creds["client_id"], creds["client_secret"])
    refresh_token = get_user_refresh_token(username)
    token_response = exchange_refresh_token_for_access_token(
        encoded_credentials, refresh_token
    )
    return token_response


if __name__ == "__main__":
    username = sys.argv[1]
    access_token = get_access_token(username)



