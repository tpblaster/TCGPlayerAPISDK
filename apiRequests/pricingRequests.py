import json
from errors import InvalidBearerToken, InvalidListLength, InvalidPricingRequest
import requests


# This endpoint takes a product condition id or a list of them and returns market data for them
# if you want pricing data for a single id then then use single_sku_market_price
# you can pass up to 250 sku ids into this endpoint


def list_sku_market_price(bearer: str, sku_list: list):
    if len(sku_list) > 250 or len(sku_list) < 2:
        raise InvalidListLength(len(sku_list))
    else:
        url = "https://api.tcgplayer.com/pricing/sku/" + ','.join(sku_list)
        headers = {'Authorization': 'Bearer ' + bearer}
        response = requests.request("GET", url, headers=headers)
        # Response if all sku ids have returned pricing
        if response.status_code == 200:
            return json.loads(response.text)["results"]
        # Response if some sku ids have returned pricing
        # TODO add an error or other handling method for some sku ids returned
        elif response.status_code == 207:
            return json.loads(response.text)["results"]
        # Response if the bearer token is invalid
        elif response.status_code == 401:
            raise InvalidBearerToken()
        # Response if all sku ids were invalid or no data was found
        elif response.status_code == 404:
            raise InvalidPricingRequest()


# Uses the same endpoint as list_sku_market_price but takes a single int sku id instead of a list

def single_sku_market_price(bearer: str, sku: int):
    url = "https://api.tcgplayer.com/pricing/sku/{}".format(sku)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Response if the sku id passed has pricing
    if response.status_code == 200:
        return json.loads(response.text)["results"][0]
    # Response if the bearer token is invalid
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Response if the sku id was invalid or no data was found
    elif response.status_code == 404:
        raise InvalidPricingRequest()
