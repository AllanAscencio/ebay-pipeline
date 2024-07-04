import logging
import json
import re
from retrieve_refresh_token_mongo.get_access_token import get_access_token
from eps_image_upload.upload_external_imageURL import upload_image_from_url
from upload_client_items.bulk_create_inventory_items import create_inventory_items
from upload_client_items.create_replace_inventory_item_group import create_inventory_group
from upload_client_items.bulk_create_offer import create_offer_from_inventory_items
from upload_client_items.publish_inventory_offer import publish_offer_inventory_group
from ebay_policies.get_fullfilment_policy import get_policy
from ebay_policies.get_payment_policy import get_payment_policy
from ebay_policies.get_return_policy import get_return_policy
from upload_client_items.get_inventory_locations import get_location_key
from check_for_new_records import check_new_records

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    
def run_ebay_pipeline(user_name, items, inv_item_group, bulk_offer, data):
    logging.info("Starting the eBay pipeline process")
    # Step 0: Check for new records in MongoDB
    # try:
    #     check_new_records()
    
    # Step 1: Get Access Token
    try:
        access_token_info = get_access_token(user_name)
        access_token = access_token_info['access_token']
        logging.info(f"Access token retrieved successfully")
    except Exception as e:
        logging.error(f"Failed to retrieve access token: {e}")
        print(access_token_info)

    # Step 2: Handle image upload (multiple URLs)
    image_urls_input = input("Are there any pictures you wish to upload to EPS? If yes, please input the URLs separated by commas (or type 'No' to skip): ")

    if image_urls_input.lower() != "no":
        image_urls = [url.strip() for url in re.split(r',\s*', image_urls_input) if url.strip()]
        uploaded_image_urls = []
        access_token = get_access_token(user_name)['access_token']

        for idx, url in enumerate(image_urls):
            try:
                output = upload_image_from_url(url, f"message_{idx}", access_token)
                logging.info(f"Image uploaded successfully: {output}")
                uploaded_image_url = output['SiteHostedPictureDetails']['FullURL']
                uploaded_image_urls.append(uploaded_image_url)
            except Exception as e:
                logging.error(f"Failed to upload image {url}: {e}")
        
        # Insert the uploaded image URLs into the data variable
        data['imageUrls'] = uploaded_image_urls
        
    else:
        logging.info("Skipping image upload step")
        img_urls = []

        
    # Step 3: Get merchantLocationKey
    try:
        response = get_location_key(access_token)
        response_json = json.loads(response.content.decode('utf-8'))
        merchant_location_key = response_json['locations'][0]['merchantLocationKey']
        logging.info(f"merchantLocationKey retrieved successfully: {merchant_location_key}")
    except Exception as e:
        logging.error(f"Failed to retrieve merchant location key: {e}")


    # Step 4: Retrieve policies
    try:
        fulfillment_policy_id = get_policy(access_token) #rename
        payment_policy_id = get_payment_policy(access_token)
        return_policy_id = get_return_policy(access_token)
        logging.info(f"Policies retrieved: Fulfillment: {fulfillment_policy_id}, Payment: {payment_policy_id}, Return: {return_policy_id}")
    except Exception as e:
        logging.error(f"Failed to retrieve policies: {e}")
        return

    # Update bulk_offer with the retrieved policy IDs
    for offer in bulk_offer:
        offer['listingPolicies']['fulfillmentPolicyId'] = fulfillment_policy_id
        offer['listingPolicies']['paymentPolicyId'] = payment_policy_id
        offer['listingPolicies']['returnPolicyId'] = return_policy_id
        offer['merchantLocationKey'] = merchant_location_key

    # Step 5: Create inventory items
    try:
        response = create_inventory_items(access_token, items)
        logging.info(f"Inventory items created successfully")
    except Exception as e:
        logging.error(f"Failed to create inventory items: {e}")
        return

    # Step 6: Create an inventory item group
    try:
        response_group = create_inventory_group(access_token, inv_item_group, data)
        if response_group.status_code == 204:
            logging.info(f"Inventory item group created successfully {response_group}")
        else:
            response_dict = json.loads(response_group.text)
            message = response_dict['errors'][0]['message']
            logging.error(f"Failed to create inventory group: {response_group} - {message}")
    except Exception as e:
        logging.error(f"Failed to create inventory item group: {e}")
        return

    # Step 7: Create an offer for the inventory items
    try:
        response_offer = create_offer_from_inventory_items(access_token, bulk_offer)
        response_dict = json.loads(response_offer.text)
        responses = response_dict['responses']
        if response_offer.status_code == 200:
            logging.info(f"Bulk create offer successful {response_offer}")
            
        else:
            for response in responses:
                if response['errors']:  # Check if there are any errors
                    message = response['errors'][0]['message']
                    logging.error(f"SKU: {response['sku']} - Message: {message}")
    except Exception as e:
        logging.error(f"Failed to create offer: {e}")
        return

    # Step 8: Publish the offer
    try:
        response_publish = publish_offer_inventory_group(access_token, inv_item_group)
        if response_publish.status_code == 200 or response_publish.status_code == 204:
            logging.info(f"Offer published successfully: {response_publish}")
        else:
             print(response_publish.__dict__)
             logging.error(f"Failed to publish offer: status {response_publish.status_code} - {message}")
    except Exception as e:
        response_dict = json.loads(response_publish.text)
        logging.error(f"""Failed to publish offer due to an exception: {response_dict.text}, {response_dict}""")



if __name__ == "__main__":
    user_name = "marihoog34"
    items = [
        {
            "sku": "test-obj20",
            "locale": "en_US",
            "product": {
                "title": "Italian T-shirt",
                "aspects": {
                    "Brand": ["Danbury Mint"],
                    "Country/Region of Manufacture": ["United States"],
                    "Type": ["T-Shirt"],
                    "Material": ["Cotton"],
                    "Theme": ["Boston Terriers"],
                    "Color": ["Black"],
                    "Size": ["Large"],
                },
                "description": "",
                "imageUrls": [
                    "https://i5.walmartimages.com/seo/Hfyihgf-Men-s-Muscle-Fit-Dress-Shirts-Wrinkle-Free-Solid-Long-Sleeve-Formal-Shirt-Business-Casual-Button-Down-Shirt-Red-L_57813b9a-90b9-4bc6-ae9d-ea54aed2fa3a.c6c66cd76dcfccb0d0913273e05222b2.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF",
                    "https://i5.walmartimages.com/seo/Hfyihgf-Men-s-Muscle-Dress-Shirts-Slim-Fit-Stretch-Formal-Shirt-Business-Short-Sleeve-Casual-Button-Down-Shirt-Red-XL_c4a3ce2c-1d34-4b02-877d-0fef0d0a6b25.cc99b0fc7dc8185c1d739d97022a3c67.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF"
                ],
            },
            "condition": "USED_EXCELLENT",
            "conditionDescription": "Worn a couple times, almost new",
            "availability": {"shipToLocationAvailability": {"quantity": 2}},
        }
        # {
        #     "sku": "test-obj13",
        #     "locale": "en_US",
        #     "product": {
        #         "title": "Italian T-shirt 2",
        #         "aspects": {
        #             "Brand": ["Danbury tniM"],
        #             "Country/Region of Manufacture": ["United States"],
        #             "Type": ["T-Shirt"],
        #             "Material": ["Coton"],
        #             "Theme": ["Marvel"],
        #             "Color": ["Red"],
        #             "Size": ["Medium"],
        #         },
        #         "description": "Joe Pavelski bobblehead from the 2015-16 season, commemorating the 25th season of the San Jose Sharks. New in box.",
        #         "imageUrls": [
        #             "https://cdn4.volusion.store/ba3tg-hs2vg/v/vspfiles/photos/av-antonio-2.jpg?v-cache=1706003778"
        #         ],
        #     },
        #     "condition": "USED_EXCELLENT",
        #     "availability": {"shipToLocationAvailability": {"quantity": 1}},
        # },
    ]
    data = {
        "title": "Test Red Shirts",
        "aspects": {
                "Condition": ["A brand-new, unused, and unworn item (including handmade items)"],
                "Pattern": ["Striped"],
                "Sleeve Length": ["Long Sleeve"],
                "Neckline": ["Collared"],
                "Closure": ["Button"],
                "Occasion": ["Business", "Casual", "Formal", "Party/Cocktail", "Travel", "Wedding"],
                "Garment care": ["Machine Washable"],
                "Pit to pit": ["See measurements", "Description", "Picture"],
                "Material": ["Polyester Blend"],
                "Fabric type": ["Woven", "Cotton"],
                "Accents": ["Button"],
                "Vintage": ["No"],
                "Fit": ["Slim"],
                "Brand": ["Italian Designed"],
                "Size Type": ["Small", "Medium", "Large"],
                "Department": ["Men"],
                "Type": ["Button-Up"],
                "Collar style": ["Spread"],
                "Model": ["Limited Edition"],
                "Theme": ["Colorful", "Couture", "Cowboy", "Dad", "Designer", "Hip Hop", "Hipster", "Italian", "Sports", "Wedding", "Western"],
                "Style": ["Button-Front"],
                "Features": ["All Seasons", "Breathable", "Easy Care", "Limited Edition", "Stretch", "UV Protection"],
                "Season": ["Fall", "Spring", "Summer", "Winter"],
                "Product Line": ["Limited Edition"]
    }, 
        "description": """<div style="text-align: center; font-family: Arial, sans-serif;">
    <p style="color: #d9534f; font-weight: bold;">WE SHIP FAST!! SAME DAY OR NEXT BUSINESS DAY!</p>
    <p>37% cotton, 60% polyester, 3% elastic spandex</p>
    <p>There is no such thing as a standard fit/size between brands. Measure something you wear now and compare it with the measurements for size selection to make your shopping experience pleasant and easy!</p>
    <p style="color: #777; font-style: italic;">MEASUREMENTS ARE APPROXIMATE</p>
</div>
""",
                                    
        "variantSKUs": ["test-obj20",],
        "imageUrls": [
            "https://i5.walmartimages.com/seo/Hfyihgf-Men-s-Muscle-Fit-Dress-Shirts-Wrinkle-Free-Solid-Long-Sleeve-Formal-Shirt-Business-Casual-Button-Down-Shirt-Red-L_57813b9a-90b9-4bc6-ae9d-ea54aed2fa3a.c6c66cd76dcfccb0d0913273e05222b2.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF",
            "https://i5.walmartimages.com/seo/Hfyihgf-Men-s-Muscle-Dress-Shirts-Slim-Fit-Stretch-Formal-Shirt-Business-Short-Sleeve-Casual-Button-Down-Shirt-Red-XL_c4a3ce2c-1d34-4b02-877d-0fef0d0a6b25.cc99b0fc7dc8185c1d739d97022a3c67.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF"
        ],
        "variesBy": {
            "specifications": [
                {"name": "Color", "values": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Brown", "Black"]},
                {"name": "Size", "values": ["Small", "Medium", "Large"]},
            ]
        },
    }
    inv_item_group = 'test_shirts_01'
    bulk_offer = [
        {
            "sku": "test-obj20",
            "marketplaceId": "EBAY_US",
            "format": "FIXED_PRICE",
            "pricingSummary": {
                "price": {
                    "value": "10.00",  
                    "currency": "USD",
                }
            },
            "listingPolicies": {
                "fulfillmentPolicyId": "241421042010",
                "paymentPolicyId": "241420767010",
                "returnPolicyId": "241420844010",
            },
            "categoryId": "30120",
            "merchantLocationKey": "DISABLED",
        },
        # {
        #     "sku": "test-obj11",
        #     "marketplaceId": "EBAY_US",
        #     "format": "FIXED_PRICE",
        #     "listingDescription": "Complete details about the item",
        #     "pricingSummary": {
        #         "price": {
        #             "value": "10.00", 
        #             "currency": "USD",
        #         }
        #     },
        #     "listingPolicies": {
        #         "fulfillmentPolicyId": "241421042010",
        #         "paymentPolicyId": "241420767010",
        #         "returnPolicyId": "241420844010",
        #     },
        #     "categoryId": "30120",
        #     "merchantLocationKey": "DISABLED",
        # },
    ]
    message_id = 'test_message'
    run_ebay_pipeline(user_name, items, inv_item_group, bulk_offer, data)

