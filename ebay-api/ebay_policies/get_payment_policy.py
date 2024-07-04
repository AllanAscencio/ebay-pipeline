import requests
from retrieve_refresh_token_mongo import get_access_token
import re

api_url = 'https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=EBAY_US'


def get_payment_policy(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Content-Language' : 'en-US',
        'Accept': 'application/json',
    }

    response = requests.get(api_url, headers=headers)
    match = re.search(r'"paymentPolicyId":"(\d+)"', response.text)
    if match:
        return_policy_id = match.group(1)
        return return_policy_id


if __name__ == "__main__":
    ebay_username = "2011allan94"
    access_token = get_access_token(ebay_username)["access_token"]
    response = get_payment_policy(access_token)


# Example output

# {"total":1,"paymentPolicies":[{"name":"payment_pol_test","description":"Payment policy test","marketplaceId":"EBAY_US",
# "categoryTypes":[{"name":"ALL_EXCLUDING_MOTORS_VEHICLES","default":false}],"paymentMethods":[],"immediatePay":true,"paymentPolicyId":"241420767010"}]}