import requests
import json
from auth.get_access_token import get_access_token


api_url = f"https://api.ebay.com/sell/inventory/v1/bulk_create_offer"


def create_offer_from_inventory_items(access_token, items):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Language": "en-US",
    }

    data = {"requests": items}

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response


if __name__ == "__main__":
    username = ""
    items = ''
    access_token = get_access_token(username)["access_token"]
    response = create_offer_from_inventory_items(access_token, items)
    print(response, response.text)