import requests
from auth.get_access_token import get_access_token


def publish_offer(access_token, offer_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish/"

    response = requests.post(api_url, headers=headers)
    return response


if __name__ == "__main__":
    offer_id = "425069683016"
    username = ""
    access_token = get_access_token(username)["access_token"]
    response = publish_offer(access_token, offer_id)
    print(response)
