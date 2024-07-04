import functions_framework
import hashlib
import flask
from flask import jsonify

# I used GCF [Google Cloud Functions]
verification_token = "VtBAkgfeY7ALqezOy2LOVZcoNjdhO7ci54as5O_g"
endpoint_url = 'https://us-central1-project-name-66666.cloudfunctions.net/ebay-account-deletion-notifications/api/ebay-challenge'

@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    if request.path == '/api/ebay-challenge':
        # Handle GET requests
        if request.method == 'GET':
            # eBay challenge verification logic
            challenge_code = request.args.get('challenge_code')
            if not challenge_code:
                return jsonify({"error": "Missing challenge_code"}), 400
            
            hash_input = f"{challenge_code}{verification_token}{endpoint_url}".encode('utf-8')
            challenge_response = hashlib.sha256(hash_input).hexdigest()
            
            return jsonify({"challengeResponse": challenge_response}), 200
        
        # Handle POST requests
        elif request.method == 'POST':
            # Example POST logic for /api/ebay-challenge, adapting the account deletion logic
            data = request.json
            print("Received data:", data)
            
            # Implement processing of account deletion, maybe to be saved in mongo, 
            # postgress or any other DB, or in a table in GBQ
            
            return jsonify({"status": "success"}), 201

    else:
        # Handling for unsupported paths or methods
        return jsonify({"error": "Unsupported route or method"}), 404