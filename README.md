# eBay API Integration

Automated integration for managing eBay store inventory, offers, and publishing processes.

## Built With

- Python
- requests
- pymongo

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher installed.
- `requests` and `pymongo` libraries installed.
- [Created developer account](https://developer.ebay.com/join)
- Once you have created your developer account you should be able to see your [credentials here](https://developer.ebay.com/my/keys)
- Normal account as seller on ebay
- A `config.json` file in your project directory containing eBay API credentials and other necessary configuration details.

### Installation

1. **Clone the repository:**
   \```bash
   git clone <repository-url>
   cd ebay-api
   \```

2. **Install required Python packages:**
   \```bash
   pip install -r requirements.txt
   \```

3. **Configuration:**
   Ensure your `config.json` is properly configured with the correct eBay API credentials and redirect URIs:
   - `client_id` and `client_secret`: Your eBay API credentials.
   - `redirect_uri`: The URI to which eBay will send the response of the OAuth process.
   - `scopes`: Specific permissions your application needs (as space-separated values).

## Usage

### Customer Authentication

![Authorization Grant Flow](https://developer.ebay.com/api-docs/res/resources/images/ebay-rest/authorization_code_650x486.png)

To interact with a customer's eBay store, we use the [Authorization Code Grant Flow](https://developer.ebay.com/api-docs/static/oauth-authorization-code-grant.html):

1. The customer goes to a specific eBay link to authenticate and gets redirected to our app.
2. We store the authorization code from the customer and exchange it for a refresh token in our database. (User tokens are short-lived; refresh tokens are long-lived, expiring in 18 months.)
3. Our process is divided into two services:
   - The first service obtains and securely stores the authorization code.
   - The second service uses the stored authorization code to retrieve an access token for future API calls.

### Inventory and Listing

Before running the pipeline, follow these steps:

1. Ensure the authorization link was approved by the user's eBay account to extract the refresh token from MongoDB.
2. Install all the requirements.

Inside `console.py`:

3. Ensure the `user_name` is filled and corresponds to a user stored in MongoDB.

4. Fill the `items` variable with valid SKU, locale, and product details. The `product` key should have descriptions, including aspects such as:
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
   will cause an error and break the pipeline.

   Note: The description at this level can be omitted, as it will be filled later when creating the inventory item group, similar to the `imageUrls` key.

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

9. Run the pipeline at ebay-api level with the command python -m console. Here, after it retrieves the token is going to ask if you need to use eBays EPS system, if you need to use ebay's EPS you will be prompted to write the urls separated by commas. Remember the urls need to use http and they have requirements on the size as well. For more information on this topic you can visit [eBay EPS](https://developer.ebay.com/devzone/xml/docs/Reference/eBay/UploadSiteHostedPictures.html). If you do not want to use ebay EPS you want to go into the variable call "data" and hardcode the url links inside the ImageUrl key.

### Compliance: Account Deletion Notifications

Currently hosted on [Google Cloud Functions](https://console.cloud.google.com/functions/details/us-central1/ebay-account-deletion-notifications?env=gen2&project=keen-snow-373818&tab=metrics).


## Considerations

- Ensure `config.json` is not stored in a public repository or an insecure location.
- Handle your eBay credentials securely to prevent unauthorized access.


## 📝 License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.
