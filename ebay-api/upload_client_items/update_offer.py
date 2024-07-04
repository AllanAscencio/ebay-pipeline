import requests
import json
from auth.get_access_token import get_access_token

# 425069682016
# 425069683016

api_url = f'https://api.ebay.com/sell/inventory/v1/offer/425069682016'
config_path = "utils/config.json"
access_token = main(config_path)['access_token']


def update_offer(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Content-Language' : 'en-US'
    }

    data = {
        "availableQuantity": 2,
        "categoryId": "57991",
        "listingDescription": "description",
        "listingPolicies": {
                        "fulfillmentPolicyId": "241421042010",
                        "paymentPolicyId"    : "241420767010",
                        "returnPolicyId"     : "241420844010"
                    },
        "pricingSummary": {
            "price": {
                "currency": "USD",
                "value": "40.00"
            }
        },
        "merchantLocationKey": "test_location",
        "quantityLimitPerBuyer": 1,
        "includeCatalogProductDetails": True
    }      

    response = requests.put(api_url, headers=headers, data=json.dumps(data))
    print(response, response.text)
    return response


if __name__ == "__main__":
    # update_offer(access_token)

    # Output
    #<204>