import requests
from retrieve_refresh_token_mongo import get_access_token
import re

api_url = 'https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_US'


def get_policy(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Content-Language' : 'en-US',
        'Accept': 'application/json',
    }

    response = requests.get(api_url, headers=headers)
    match = re.search(r'"fulfillmentPolicyId":"(\d+)"', response.text)
    if match:
        return_policy_id = match.group(1)
        return return_policy_id


if __name__ == "__main__":
    ebay_username = "2011allan94"
    items = ''
    access_token = get_access_token(ebay_username)["access_token"]
    response = get_policy(access_token)
    print(response, response.text)





# Example Output

# "returnPolicyId": "241420844010",
# {"total":1,"fulfillmentPolicies":[{"name":"shipping_pol_test","description":"Shipping test policy","marketplaceId":"EBAY_US",
# "categoryTypes":[{"name":"ALL_EXCLUDING_MOTORS_VEHICLES","default":false}],"handlingTime":{"value":2,"unit":"DAY"},
# "shipToLocations":{},"shippingOptions":[{"optionType":"DOMESTIC","costType":"FLAT_RATE","shippingServices":[{"sortOrder":1,"shippingCarrierCode":"USPS",
# "shippingServiceCode":"USPSMedia","shippingCost":{"value":"0.0","currency":"USD"},"additionalShippingCost":{"value":"0.0","currency":"USD"},"freeShipping":true,
# "buyerResponsibleForShipping":false,"buyerResponsibleForPickup":false}],"shippingDiscountProfileId":"0","shippingPromotionOffered":false}],"globalShipping":false,
# "pickupDropOff":false,"freightShipping":false,"fulfillmentPolicyId":"241421042010"}]}