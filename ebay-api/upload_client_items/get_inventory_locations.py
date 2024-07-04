import requests
from auth.get_access_token import get_access_token


api_url = f'https://api.ebay.com/sell/inventory/v1/location'

def get_location_key(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    

    response = requests.get(api_url, headers=headers)
    return response


if __name__ == "__main__":
    ebay_username = "2011allan94"
    items = ''
    access_token = get_access_token(ebay_username)["access_token"]
    response = get_location_key(access_token)