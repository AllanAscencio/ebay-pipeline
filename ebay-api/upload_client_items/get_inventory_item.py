import requests
# from ebay_client_scopes_oauth.oauth_workflow import main

# sku_item_test = 'test-obj1'

api_url = 'https://api.ebay.com/sell/inventory/v1/bulk_get_inventory_item'
# config_path = "utils/config.json"
# access_token = main(config_path)['access_token']


def get_inventory_item(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    payload = {
        "requests": [
            {"sku": "test-obj2"},
            {"sku": "test-obj1"}
        ]
    }

    api_url = 'https://api.ebay.com/sell/inventory/v1/bulk_get_inventory_item'
    response = requests.post(api_url, headers=headers, json=payload)
    return response, response.text, response.json()

print(get_inventory_item(access_token))

