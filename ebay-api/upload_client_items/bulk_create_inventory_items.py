import requests
import json
from auth.get_access_token import get_access_token

api_url = "https://api.ebay.com/sell/inventory/v1/bulk_create_or_replace_inventory_item"


def create_inventory_items(access_token, items):
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
    ebay_username = "2011allan94"
    items = ''
    access_token = get_access_token(ebay_username)["access_token"]
    response = create_inventory_items(access_token, items)
