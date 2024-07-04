import requests
import json
from auth.get_access_token import get_access_token


api_url = "https://api.ebay.com/sell/inventory/v1/offer/publish_by_inventory_item_group"


def publish_offer_inventory_group(access_token, inventory_item_group_key="test"):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "inventoryItemGroupKey": inventory_item_group_key,
        "marketplaceId": "EBAY_US",
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response


if __name__ == "__main__":
    # Example usage:
    username = "..."
    access_token = get_access_token(username)
    response = publish_offer_inventory_group(access_token, "test")

    if response.status_code == 200:
        print("Success:", response.text)
    else:
        print("Failed:", response.status_code, response.text)
