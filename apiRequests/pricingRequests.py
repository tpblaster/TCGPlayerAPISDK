import json
import requests
from cardClasses.pricingDataClasses import SkuPricingData
from errors import InvalidBearerToken, InvalidListLength, InvalidPricingRequest, InvalidGroupId, NoDataFoundForGroup


# This endpoint takes a product condition id or a list of them and returns market data for them
# if you want pricing data for a single id then then use single_sku_market_price
# you can pass up to 250 sku ids into this endpoint
# expects a list of ints


def list_sku_market_price(bearer: str, sku_list: list):
    if len(sku_list) > 250 or len(sku_list) < 2:
        raise InvalidListLength(len(sku_list))
    else:
        url = "https://api.tcgplayer.com/pricing/sku/" + ','.join(map(str, sku_list))
        headers = {'Authorization': 'Bearer ' + bearer}
        response = requests.request("GET", url, headers=headers)
        # Response if all sku ids have returned pricing, returns list of pricing dicts
        # TODO may want to use the class from pricingDataClasses to parse result
        if response.status_code == 200:
            return json.loads(response.text)["results"]
        # Response if some sku ids have returned pricing, returns SkuPricingData object list
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
    # Response if the sku id passed has pricing, returns SkuPricingData object
    if response.status_code == 200:
        return json.loads(response.text)["results"][0]
    # Response if the bearer token is invalid
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Response if the sku id was invalid or no data was found
    elif response.status_code == 404:
        raise InvalidPricingRequest()


def get_all_price_group(bearer: str, group_id: int):
    url = "https://api.tcgplayer.com/pricing/group/{}".format(group_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Request was successful and data is returned, returns list of pricing dict from api
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Request had an invalid group id and is either 0 or less than 0
    elif response.status_code == 400:
        raise InvalidGroupId()
    # Request returned no data or group is above 0 but invalid
    elif response.status_code == 404:
        raise NoDataFoundForGroup()
