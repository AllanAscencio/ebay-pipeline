import requests
import json
from retrieve_refresh_token_mongo import get_access_token


api_url = f'https://api.sandbox.ebay.com/sell/account/v1/return_policy'


def create_inventory(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    
    data = {
    "name": "test_shirt_policies",
    "marketplaceId": "EBAY_US",
    "refundMethod": "MONEY_BACK",
    "returnsAccepted":True,
    "returnShippingCostPayer": "SELLER",
    "returnPeriod": {
        "value": 30,
        "unit": "DAY"
    }
}

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    print(response, response.text)

if __name__ == "__main__":
    username = ""
    access_token = get_access_token(username)["access_token"]
    response = create_inventory(access_token)
    print(response, response.text)