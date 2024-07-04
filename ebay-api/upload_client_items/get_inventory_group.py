import requests
# from ebay_client_scopes_oauth.oauth_workflow import main


api_url = 'https://api.ebay.com/sell/inventory/v1/inventory_item_group/test'
# config_path = "utils/config.json"
# access_token = main(config_path)['access_token']


def get_inventory_group(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.get(api_url, headers=headers)
    print(response.text)

get_inventory_group(access_token)

