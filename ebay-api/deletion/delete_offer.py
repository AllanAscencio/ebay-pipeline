import requests
from ebay_client_scopes_oauth.oauth_workflow import main



api_url = 'https://api.ebay.com/sell/inventory/v1/offer/426388216016'
config_path = "utils/config.json"
access_token = main(config_path)['access_token']


def delete_offer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }


    response = requests.delete(api_url, headers=headers)
    return response, response.text

print(delete_offer(access_token))

