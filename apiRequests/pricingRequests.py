import json

import requests

from errors import InvalidBearerToken, InvalidListLength, InvalidPricingRequest, InvalidGroupId, NoDataFoundForGroup


# This endpoint takes a product condition id or a list of them and returns market data for them
# if you want pricing data for a single id then then use single_sku_market_price
# you can pass up to 250 sku ids into this endpoint
# expects a list of ints


def get_sku_list_market_price(bearer: str, sku_list: list):
    if len(sku_list) > 250 or len(sku_list) < 2:
        raise InvalidListLength(len(sku_list))
    else:
        url = "https://api.tcgplayer.com/pricing/sku/" + ','.join(map(str, sku_list))
        headers = {'Authorization': 'Bearer ' + bearer}
        response = requests.request("GET", url, headers=headers)
        # Response if all sku ids have returned pricing, returns list of pricing dicts
        # The success marker will evaluate to true
        # TODO may want to use the class from pricingDataClasses to parse result
        if response.status_code == 200:
            return json.loads(response.text)
        # Response if some sku ids have returned pricing, returns SkuPricingData object list
        # Those that were not found are returned in the error message
        # The success marker will evaluate to false
        # TODO add an error or other handling method for some sku ids returned, different handling for 200 vs 207
        elif response.status_code == 207:
            return json.loads(response.text)
        # Response if the bearer token is invalid
        elif response.status_code == 401:
            raise InvalidBearerToken()
        # Response if all sku ids were invalid or no data was found
        elif response.status_code == 404:
            raise InvalidPricingRequest()


# Uses the same endpoint as list_sku_market_price but takes a single int sku id instead of a list

def get_single_sku_market_price(bearer: str, sku: int):
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


# This endpoint takes a group id and returns all pricing data for that group
# Product Ids will be repeated for each subTypeName that is available even if there is no pricing data

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
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request returned no data or group is above 0 but invalid
    elif response.status_code == 404:
        raise NoDataFoundForGroup()


# Takes a list of product ids and returns pricing data
# Please pass the product id list as a list of ints
# Each product id will return 2 dict entries, one will be subTypeName Normal and one will be foil
# If no data exists for one all values will be null

def get_product_list_market_price(bearer: str, product_list: list):
    # Handles potential 400 responses
    if len(product_list) > 250 or len(product_list) < 2:
        raise InvalidListLength(len(product_list))
    url = "https://api.tcgplayer.com/pricing/product/" + ','.join(map(str, product_list))
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Returns all data if every product id had data
    if response.status_code == 200:
        return json.loads(response.text)
    # Returns all data found but some product ids had no data, those with no data are indicated in the error section
    elif response.status_code == 207:
        return json.loads(response.text)
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # All ids were invalid or no data was found
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Takes a single product id and returns a list of all pricing data for each subTypeName
# TODO redo code to handle single length lists, remove extraneous functions

def get_single_product_market_price(bearer: str, product_id: int):
    url = "https://api.tcgplayer.com/pricing/product/{}".format(product_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Returns a list of pricing data associated with the given product id
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found or the product id was invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Takes a list of product ids and returns buylist data
# Takes a list of integer based product ids

def get_product_list_buylist_price(bearer: str, product_list: list):
    # Handles potential 400 responses
    if len(product_list) > 250 or len(product_list) < 2:
        raise InvalidListLength(len(product_list))
    url = "https://api.tcgplayer.com/pricing/buy/product/" + ','.join(map(str, product_list))
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # All product ids had data and it is all returned
    if response.status_code == 200:
        return json.loads(response.text)
    # Some product ids had data, those that didn't are returned in the error section
    elif response.status_code == 207:
        return json.loads(response.text)
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found or all product ids were invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Takes a single product id and returns all buylist data for skus related to the id

def get_single_product_buylist_price(bearer: str, product_id: int):
    url = "https://api.tcgplayer.com/pricing/buy/product/{}".format(product_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Request was successful
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    elif response.status_code == 401:
        raise InvalidBearerToken()
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Takes an int based list of sku ids and returns buylist data for them

def get_sku_list_buylist_price(bearer: str, sku_list: str):
    # Handles potential 400 responses
    if len(sku_list) > 250 or len(sku_list) < 2:
        raise InvalidListLength(len(sku_list))
    url = "https://api.tcgplayer.com/pricing/buy/sku/" + ','.join(map(str, sku_list))
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Request was successful, every sku is returned with data
    if response.status_code == 200:
        return json.loads(response.text)
    # Some sku ids did not have data and are returned in the error section
    elif response.status_code == 207:
        return json.loads(response.text)
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found for all sku ids or all sku ids were invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Takes a single sku id and returns pricing data

def get_single_sku_buylist_price(bearer: str, sku_id: int):
    url = "https://api.tcgplayer.com/pricing/buy/sku/{}".format(sku_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found for the sku id or the sku id was invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()


# Gets buylist prices for a set based on the group id

def get_group_buylist_price(bearer: str, group_id: int):
    url = "https://api.tcgplayer.com/pricing/buy/group/{}".format(group_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Request had an invalid group id and is either 0 or less than 0
    elif response.status_code == 400:
        raise InvalidGroupId()
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found for the group id or it was invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()
