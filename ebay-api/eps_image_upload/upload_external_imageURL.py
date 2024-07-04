import requests
import os
import sys
from image_upload.utils import parse_xml_response
from retrieve_refresh_token_mongo import get_access_token

EPS_URL = "https://api.ebay.com/ws/api.dll"

# Headers
HEADERS = {
    "X-EBAY-API-CALL-NAME": "UploadSiteHostedPictures",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-RESPONSE-ENCODING": "XML",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "X-EBAY-API-DETAIL-LEVEL": "0",
    "Cache-Control": "no-cache",
    "Content-Type": "multipart/form-data",
}


def construct_xml_payload(image_url, picture_name, message_id, auth_token):
    # XML Payload
    return f"""
        <?xml version="1.0" encoding="utf-8"?>
        <UploadSiteHostedPicturesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
            <eBayAuthToken>{auth_token}</eBayAuthToken>
            </RequesterCredentials>
            <WarningLevel>High</WarningLevel>
            <ExternalPictureURL>{image_url}</ExternalPictureURL>
            <PictureName>{picture_name}</PictureName>
            <MessageID>{message_id}</MessageID>
        </UploadSiteHostedPicturesRequest>
        """


def upload_image_from_url(image_url, message_id, auth_token):
    picture_name = image_url.split("/")[-1].split(".")[0]
    xml_payload = construct_xml_payload(image_url, picture_name, message_id, auth_token)

    response = requests.post(EPS_URL, headers=HEADERS, data=xml_payload)
    if response.status_code == 200:
        print("API call successful")
        response_data = parse_xml_response(response)
        if response_data["Ack"] == "Failure":
            print("Failed to upload image:", response_data["Errors"]["LongMessage"])
        return response_data
    else:
        print("API call failed.")
        response_data = {"StatusCode": response.status_code, "XML": response.text}
        return response_data


if __name__ == "__main__":
    url = sys.argv[1]
    username = sys.argv[2]
    auth_token = get_access_token(username)["access_token"]
    message_id = "test"
    output = upload_image_from_url(url, message_id, auth_token)
    print(output)


# command execution inside ebay-api folder
# python -m image_upload.upload_external_imageURL https://url_of_image.png ebay_user_name

# Example Output

# API call successful
# {'StatusCode': 200, 'Ack': 'Success', 'CorrelationID': 'test', 'SiteHostedPictureDetails': {'PictureName': 'back_01_og_wobg_wom', 'PictureSet': 'Standard', 'PictureFormat': 'PNG',
# 'FullURL': 'https://i.ebayimg.com/00/s/MTMzM1gxMDAw/z/xqcAAOSwT4VmQhGe/$_1.PNG?set_id=2', 'BaseURL': 'https://i.ebayimg.com/00/s/MTMzM1gxMDAw/z/xqcAAOSwT4VmQhGe/$_',
# 'PictureSetMember': '\n            ', 'ExternalPictureURL': 'https://storage.googleapis.com/client-dev-bucket/6413cf5402ff75754ba528f0/d4f16b5f-a7a6-13da-e2f1-54c4cb2f788a/back_01_og_wobg_wom.png',
# 'UseByDate': '2024-06-12T13:11:57.643Z'}, 'Timestamp': '2024-05-13T13:11:58.260Z'}

