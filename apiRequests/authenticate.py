import json
import requests
from errors import InvalidBearerRequest

# Takes public and private keys to create a bearer token which is used to authenticate requests to the api
# Please store your keys in a safe place, not in plain text
# Raises InvalidBearerRequest if the request fails


def create_bearer_token(client_id: str, client_secret: str):
    url = "https://api.tcgplayer.com/token"
    payload = "grant_type=client_credentials&client_id={}&client_secret={}".format(client_id, client_secret)
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        return json.loads(response.text)["access_token"]
    else:
        raise InvalidBearerRequest()
