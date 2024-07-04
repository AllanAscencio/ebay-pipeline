import requests
from ebay_client_scopes_oauth.oauth_workflow import main

# sku_item_test = 'test-obj1'

api_url = 'https://api.ebay.com/sell/inventory/v1/offer/425069683016'
config_path = "utils/config.json"
access_token = main(config_path)['access_token']


def get_inventory_item(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }


    response = requests.get(api_url, headers=headers)
    return response, response.text, response.json()

print(get_inventory_item(access_token))

