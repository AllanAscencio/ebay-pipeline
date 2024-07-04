import requests
import json
from auth.get_access_token import get_access_token


def create_inventory_group(access_token, inv_name, data):
    api_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item_group/{inv_name}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Language": "en-US",
    }

    # Making the PUT request to create or replace an inventory item group
    response = requests.put(api_url, headers=headers, data=json.dumps(data))
    return response


if __name__ == "__main__":
    username = ""
    data = {}
    access_token = get_access_token(username)["access_token"]
    group_id = ""

    response = create_inventory_group(access_token, group_id, data)
    print(response)