import requests
from retrieve_refresh_token_mongo import get_access_token

def create_policy(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    payload = {
        "name": "tshirts_payment",
        "marketplaceId": "EBAY_US",
        "categoryTypes": [
            {
                "name": "ALL_EXCLUDING_MOTORS_VEHICLES"  # Correct category type
            }
        ],
        "paymentMethods": [
            {
                "paymentMethodType": "PERSONAL_CHECK"
            }
        ]
    }

    api_url = 'https://api.ebay.com/sell/account/v1/payment_policy'
    response = requests.post(api_url, headers=headers, json=payload)
    return response, response.text

if __name__ == "__main__":
    username = ""
    access_token = get_access_token(username)["access_token"]
    response = create_policy(access_token)
    print(response, response.text)