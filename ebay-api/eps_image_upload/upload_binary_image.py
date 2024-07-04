import requests
import os
import sys
from retrieve_refresh_token_mongo.get_access_token import get_access_token
from image_upload.utils import parse_xml_response


EPS_URL = "https://api.ebay.com/ws/api.dll"
BOUNDARY = "----FormBoundary7MA4YWxkTrZu0gW"

# Headers
EPS_HEADERS = {
    "X-EBAY-API-CALL-NAME": "UploadSiteHostedPictures",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-RESPONSE-ENCODING": "XML",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "X-EBAY-API-DETAIL-LEVEL": "0",
    "Cache-Control": "no-cache",
    "Content-Type": f"multipart/form-data; boundary={BOUNDARY}",
}


def construct_xml_payload(picture_name, message_id, auth_token, boundary=BOUNDARY):
    # XML payload
    return f"""------{BOUNDARY}
    Content-Disposition: form-data; name="XML Payload"

    <?xml version="1.0" encoding="utf-8"?>
    <UploadSiteHostedPicturesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <ebl:eBayAuthToken xmlns:ebl="urn:ebay:apis:eBLBaseComponents">{auth_token}</ebl:eBayAuthToken>
        </RequesterCredentials>
        <PictureName>Gall-{picture_name}</PictureName>
        <PictureSet>Standard</PictureSet>
        <ExtensionInDays>30</ExtensionInDays>
        <MessageID>{message_id}</MessageID>
    </UploadSiteHostedPicturesRequest>
    """


def construct_full_payload(image_data, picture_name, name, file_name, message_id, auth_token, boundary=BOUNDARY):
    
    xml_payload = construct_xml_payload(picture_name, message_id, auth_token, boundary)
    
    return (
        f"""{xml_payload}
        ------{boundary}
        Content-Disposition: form-data; name={name}; filename="{file_name}"
        Content-Type: image/png

        """.encode(
            "utf-8"
        )
        + image_data
        + f"\n------{boundary}--".encode("utf-8")
    )


def get_image_from_file(file_path):
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()
    return image_data


def upload_image_from_file(file_path, message_id, auth_token):
    image_data = get_image_from_file(file_path)
    file_name = os.path.basename(file_path)
    picture_name = file_name.split(".")[0]
    name = picture_name
    payload = construct_full_payload(
        image_data,
        picture_name,
        name,
        file_name,
        message_id,
        auth_token,
        boundary=BOUNDARY,
    )

    # POST request
    response = requests.post(EPS_URL, headers=EPS_HEADERS, data=payload)

    # Check the response
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
    file_path = sys.argv[1]
    username = sys.argv[2]
    auth_token = get_access_token(username)
    message_id = "x"
    response_data = upload_image_from_file(file_path, message_id, auth_token)
    print(response_data)
