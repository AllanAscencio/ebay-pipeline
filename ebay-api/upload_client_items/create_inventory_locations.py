import requests
from auth.get_access_token import get_access_token


def create_inv_location(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "location": {
            "address": {
                "addressLine1": "Heather hill lane",
                "addressLine2": "",
                "city": "Boca Raton",
                "stateOrProvince": "Florida",
                "postalCode": "33486",
                "country": "US",
            }
        },
        "locationInstructions": "Items ship from here.",
        "name": "Allan-test",
        "phone": "954 465 0627",
        "merchantLocationStatus": "DISABLED",
        "locationTypes": ["WAREHOUSE"],
    }

    api_url = "https://api.ebay.com/sell/inventory/v1/location/test_location"
    response = requests.post(api_url, headers=headers, json=payload)
    return response, response.text


if __name__ == "__main__":
    username = "marihoog34"
    access_token = get_access_token(username)["access_token"]
    print(create_inv_location(access_token))
