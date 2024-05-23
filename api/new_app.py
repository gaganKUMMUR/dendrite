from flask import Flask, redirect, request, session, url_for, jsonify
from flask_cors import CORS
from flask_oidc import OpenIDConnect
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from schema import schema
from core import app
import config
import requests


CORS(app)

# Configure Keycloak
app.config.update({
    'SECRET_KEY': 'your_secret_key_here',
    'OIDC_CLIENT_SECRETS': '../login_api/client_secrets.json',  # Path to your client_secrets.json file
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
})

YOUR_DOMAIN ="http://127.0.0.1:5000"
oidc = OpenIDConnect(app)

# Define the GraphiQL explorer HTML
explorer_html = ExplorerGraphiQL().html(None)


@app.route("/", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@app.route("/", methods=["POST"])
@oidc.accept_token()
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema=schema, data=data, context_value=request, debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, port=8000)
