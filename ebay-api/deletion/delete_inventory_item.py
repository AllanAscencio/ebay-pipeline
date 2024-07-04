import requests
from retrieve_refresh_token_mongo import get_access_token

# sku_item_test = 'test-obj1'

api_url = 'https://api.ebay.com/sell/inventory/v1/inventory_item/test-obj1'


def delete_offer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }


    response = requests.delete(api_url, headers=headers)
    return response, response.text

if __name__ == "__main__":
    username = ""
    access_token = get_access_token(username)["access_token"]
    response = delete_offer(access_token)
    print(response, response.text)

# v%5E1.1%23i%5E1%23p%5E3%23r%5E1%23f%5E0%23I%5E3%23t%5EUl41XzExOkM3RTlCQUYyOTcxN0I5NUY3QUEzMUJBMDRCN0UyRDVGXzJfMSNFXjI2MA%3D%3D