# eBay API Integration

Automated integration for managing eBay store inventory, offers, and publishing processes.

## Capabilities

This repository facilitates eBay integration through Python, allowing for the successful and efficient upload of listings to eBay using eBay API calls and OAuth. The tool enables detailed customization of items, with the ability to run the pipeline for automatic upload and posting.

### 1. Upload Clothing Items to the eBay Seller Platform, Ranging from Single Items to Multiple Items as a Group Offer
![image](https://github.com/user-attachments/assets/9ebf2e5e-99be-47a5-891e-9039d1bcf6ec)
![image](https://github.com/user-attachments/assets/cbd5ce3a-7dc2-41fa-a716-b7168a880abb)

### 2. Use HTML Code to Create and Modify Attractive Descriptions
![image](https://github.com/user-attachments/assets/f3f7903a-0525-40ef-9564-32a297c16423)

### 3. Additional API Calls Included:
- Update offers
- Retrieve inventory group, inventory item, inventory location, or offer
- Delete inventory item or offer
- Create payment or return policies

### 4. Additional Features:
- Incorporated eBay account deletion notifications (mandatory as per eBay requirements)
- Added a cloud function callback connected to MongoDB. Initially used in Google Cloud Functions, but the code is compatible with other cloud services like AWS.

## Quickstart

1. Obtain the user's access token to use for all API calls.
2. Decide whether the EPS (eBay Photo Services) is needed.
3. Extract the merchant location keys.
4. Retrieve the account's policy IDs.
5. Create the inventory items.
6. Create the inventory group.
7. Create the offer for the inventory items.
8. Publish the offer.

When the pipeline runs successfully, the console will display output similar to the following:
![image](https://github.com/user-attachments/assets/41e8e557-4ab1-4f1a-9e5e-44e664fb8260)

## Getting Started

To set up a local copy, follow these steps:

### Prerequisites

Before beginning, ensure the following requirements are met:

- Python 3.8 or higher installed.
- `requests` and `pymongo` libraries installed.
- [Developer account created](https://developer.ebay.com/join)
- Once the developer account is created, [view credentials here](https://developer.ebay.com/my/keys).
- A seller account on eBay.
- A `config.json` file in the project directory containing eBay API credentials and other necessary configuration details.

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ebay-api
   
2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt

3. **Configuration:**
   Ensure your `config.json` is properly configured with the correct eBay API credentials and redirect URIs:
   - `client_id` and `client_secret`: Your eBay API credentials.
   - `redirect_uri`: The URI to which eBay will send the response of the OAuth process.
   - `scopes`: Specific permissions your application needs (as space-separated values).

## Usage

### Customer Authentication

![Authorization Grant Flow](https://developer.ebay.com/api-docs/res/resources/images/ebay-rest/authorization_code_650x486.png)

To interact with a customer's eBay store, we use the [Authorization Code Grant Flow](https://developer.ebay.com/api-docs/static/oauth-authorization-code-grant.html):

1. The customer authenticates via a specific eBay link and is redirected to the application.
2. The authorization code from the customer is stored and exchanged for a refresh token in the database. (User tokens are short-lived; refresh tokens are long-lived, expiring in 18 months.)
3. The process is divided into two services:
- The first service obtains and securely stores the authorization code.
- The second service uses the stored authorization code to retrieve an access token for future API calls.

### Inventory and Listing

Before running the pipeline, follow these steps:

1. Ensure the authorization link was approved by the user's eBay account to extract the refresh token from MongoDB.
2. Install all the requirements.

Inside `console.py`:

3. Ensure the `user_name` field is populated and corresponds to a user stored in MongoDB.

4. Fill the `items` variable with valid SKU, locale, and product details. The `product` key should include descriptions covering aspects such as:
   - brand
   - country of manufacture
   - type
   - material
   - theme
   - color
   - size, etc.

   Each aspect must contain a single key-value pair. For example:
   ```json
   {
     "Size": "Large"
   }
   ```
   Having multiple values for a single key, such as:
   ```json
   {
     "Size": ["Large", "Small"]
   }
   ```
  will cause an error and disrupt the pipeline.

  Note: The description at this level can be omitted, as it will be provided later when creating the inventory item group, similar to the `imageUrls` key.

   `condition` and `conditionDescription` are optional but recommended.

   The `availability` container is optional until the seller is ready to publish an offer with the SKU. At that point, it becomes required. Availability data must also be passed if an inventory item is being updated and availability data already exists for that inventory item. Example:
   ```json
   {
     "availability": {
       "shipToLocationAvailability": {
         "quantity": 2
       }
     }
   }
   ```

5. Check the `data` variable:
   - Provide a title.
   - Provide aspects of the item(s) to be shown below the item listing.
   - Provide a description of the item(s), referred to as "Item description from the seller" at the bottom of the published listing.
   - Include the `variantSKUs` for all items in the item group (or just one). Also, provide `imageUrls` and complete the `variesBy` key, usually containing another key called `specifications` with all product variants. Example:
   ```json
   {
     "specifications": {
       "Color": ["Red", "Blue"],
       "Size": ["Small", "Medium", "Large"]
     }
   }
   ```

   Note: Each item can have ONLY ONE variant specification. For example:
   ```json
   {
     "sku": "item1",
     "size": "Small"
   }
   ```

6. Fill the `inv_item_group` variable with the inventory item group name. If you upload new items with the same group name, the previous listing will be replaced.

7. Fill the `bulk_offer` variable with details such as:
   - `sku`
   - `marketplaceId`
   - `format`
   - `pricingSummary` (including `price` with `value` and `currency`)
   - `listingPolicies` (including `fulfillmentPolicyId`, `paymentPolicyId`, `returnPolicyId`)

   Business policies (payment, return, fulfillment) must be created before publishing an offer. Example:
   ```json
   {
     "pricingSummary": {
       "price": {
         "value": 100,
         "currency": "USD"
       }
     }
   }
   ```

   Note: Sellers must be opted into Business Policies to create live eBay listings through the Inventory API.

8. Fill the `categoryId` and `merchantLocationKey` inside Bulk_offer (either specific location or "DISABLED").

9. Run the pipeline at the ebay-api level with the command python -m console. After retrieving the token, the system will prompt whether to use eBay's EPS system. If EPS is required, URLs separated by commas will need to be provided. The URLs must use HTTP and adhere to specific size requirements. For more information, visit [eBay EPS](https://developer.ebay.com/devzone/xml/docs/Reference/eBay/UploadSiteHostedPictures.html).If EPS is not used, hardcode the URL links inside the ImageUrl key in the data variable.
   
### Compliance: Account Deletion Notifications

Currently hosted on Google Cloud Functions


## Considerations

- Ensure `config.json` is not stored in a public repository or an insecure location.
- Handle your eBay credentials securely to prevent unauthorized access.


## 📝 License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.
