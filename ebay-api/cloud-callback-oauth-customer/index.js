const axios = require('axios');
const express = require('express');
const { MongoClient, ObjectID } = require('mongodb');
const app = express();

// Note: It's not secure to hardcode credentials like this in your code. Consider using environment variables or a secret manager.
// I used GCF [Google Cloud Functions] to alocate the following code
const eBayAppCredentials = {
    clientId: 'ebay-client-id',
    clientSecret: 'ebay-client-secret',
    redirectUri: 'ebay-redirect-uri',
};

const scopesList = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.marketing",
        "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.account",
        "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
        "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.finances",
        "https://api.ebay.com/oauth/api_scope/sell.reputation",
        "https://api.ebay.com/oauth/api_scope/sell.reputation.readonly",
        "https://api.ebay.com/oauth/api_scope/commerce.identity.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.stores",
        "https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
]

app.get('/ebay-auth', (req, res) => {
    const { clientId } = req.query;
    const scopes = encodeURIComponent(scopesList.join(' '));
    const authUrl = `https://auth.ebay.com/oauth2/authorize?state=${clientId}&client_id=${eBayAppCredentials.clientId}&redirect_uri=${eBayAppCredentials.redirectUri}&response_type=code&scope=${scopes}`;
    console.log(authUrl);
    res.redirect(authUrl);
});

app.get('/ebay-callback', async (req, res) => {
    console.log("/ebay-callback endpoint called");
    try {
        const { code, state } = req.query; // Assuming `code` is correctly obtained here
        console.log("code passed to callback:", code);

        // Prepare the data using URLSearchParams
        const data = new URLSearchParams({
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: eBayAppCredentials.redirectUri,
        }).toString();

        // Make the token request
        const tokenResponse = await axios.post('https://api.ebay.com/identity/v1/oauth2/token', data, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            auth: {
                username: eBayAppCredentials.clientId,
                password: eBayAppCredentials.clientSecret,
            },
        });

        const { access_token, refresh_token, expires_in } = tokenResponse.data;
        console.log("tokenResponse.data:", tokenResponse.data);
        const config = {
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };

        let user_name, user_id, account_type, registration_marketplace_id, business_account_information;
        await axios.get('https://apiz.ebay.com/commerce/identity/v1/user/', config)
            .then(response => {
                console.log('User Response Data:', response.data);
                user_name = response.data.username;
                user_id = response.data.userId;
                account_type = response.data.accountType;
                registration_marketplace_id = response.data.registrationMarketplaceId;
                business_account_information = response.data.businessAccount;
                // Process the response data here. The structure of the response data will depend on eBay's API response schema.
            })
            .catch(error => {
                console.error('Error calling eBay Commerce Identity API:', error.message);
                // Handle errors here
            });
        const uri = "mongodb+srv://mvptestingtesting111:Wa9ae5E30pg8bcry@serverlessinstance0.mnxt5.mongodb.net/test";
        const expTime = new Date(Date.now() + expires_in * 1000);
        const now = new Date();
        const client = new MongoClient(uri);
        await client.connect();

        // Specify the database and collection
        const database = client.db("backend_database");
        const collection = database.collection("client_user_table");

        const filter = { "_id": new ObjectID(state) };

        const update = {
            $set: {
                'ebay_access': {
                    clientId: state,
                    customerEbayUserId: user_id,
                    customerEbayAccountType: account_type,
                    customerEbayRegistrationMarketplaceId: registration_marketplace_id,
                    customerEbayBusinessAccountinformation: business_account_information,
                    applicationClientId: eBayAppCredentials.clientId,
                    ruName: eBayAppCredentials.redirectUri,
                    accessToken: access_token,
                    refreshToken: refresh_token,
                    expiresIn: expires_in,
                    expiresAt: expTime,
                    updatedAt: now, // Set updatedAt to current timestamp
                }
            },
            $setOnInsert: {
                createdAt: now, // Set createdAt only on insert
            }
        };

        // Set the upsert option to true for a conditional insert or update
        const options = { upsert: true };

        // Perform the update or insert operation
        const result = await collection.updateOne(filter, update, options);

        if (result.upsertedCount > 0) {
            console.log(`A new document was inserted with the userName ${user_name}.`);
        } else if (result.modifiedCount > 0) {
            console.log(`Document with userName ${user_name} was updated.`);
        } else {
            console.log(`Document with userName ${user_name} was not updated (no changes or already up-to-date).`);
        }

        let redirectUrl = 'https://intheloopai.com/';
        res.redirect(redirectUrl);
    } catch (error) {
        console.error('Error during eBay OAuth2 callback:', error.message);
        res.status(500).send('Internal Server Error');
    }
});

// Other routes...

exports.helloHttp = (req, res) => {
    // This is necessary because Cloud Functions expects the Express app to handle the request/response objects
    if (!req.path) {
        // Prepend '/' to keep query params if any
        req.url = `/${req.url}`;
    }
    return app(req, res);
};



// My google cloud functions were allocated in a url like # https://us-central1-project-name-99999.cloudfunctions.net/eBay-OAuth/ebay-callback?success=true

