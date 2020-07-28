import json

import requests

from errors import InvalidBearerToken, InvalidListLength, InvalidPricingRequest, InvalidGroupId, NoDataFoundForGroup, \
    InvalidSkuIdRequest


def get_sku_market_price(bearer: str, sku_list: list):
    """
    This endpoint takes a product condition id/sku id or a list of them and returns market data for them

    Endpoint accepts up to 250 sku ids

    Endpoint name is List SKU Market Prices

    :param bearer: string based access token
    :param sku_list: integer based list of sku ids
    :return: returns full json response with error data indicated in the error section of the object
    """
    if len(sku_list) > 250 or len(sku_list) < 1:
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


def get_all_price_group(bearer: str, group_id: int):
    """
    This endpoint takes a group id and returns all pricing data for that group

    Endpoint name is List Product Prices by Group

    :param bearer: string based access token
    :param group_id: integer based group id
    :return: returns full data for the group for every possible subTypeName
    """
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


def get_product_market_price(bearer: str, product_list: list):
    """
    Takes a list of product ids and returns pricing data for all possible subTypeName

    Endpoint name is List Product Market Prices

    :param bearer: string based access token
    :param product_list: list of integer based product ids
    :return: returns full data including potential errors in the error object section
    """
    # Handles potential 400 responses
    if len(product_list) > 250 or len(product_list) < 1:
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


def get_product_buylist_price(bearer: str, product_list: list):
    """
    Takes a list of product ids and returns buylist data

    Endpoint name is List Product Buylist Prices

    :param bearer: string based access token
    :param product_list: integer based list of product ids for data to be returned for
    :return: returns full json data with potential errors indicated in the error section of the object
    """
    # Handles potential 400 responses
    if len(product_list) > 250 or len(product_list) < 1:
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


def get_sku_buylist_price(bearer: str, sku_list: str):
    """
    Takes an int based list of sku ids and returns buylist data for them

    Endpoint name is List SKU Buylist Prices

    :param bearer: string based access token
    :param sku_list: integer based list of sku ids
    :return: returns full json data with potential errors indicated in the error section of the object
    """
    # Handles potential 400 responses
    if len(sku_list) > 250 or len(sku_list) < 1:
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


def get_group_buylist_price(bearer: str, group_id: int):
    """
    Gets buylist prices for a set based on the group id

    Endpoint name is List Product Buylist Prices by Group

    :param bearer: string based access token
    :param group_id: integer based group id
    :return: returns full product id information for the buylist prices of a group
    """
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


def get_market_price_for_single_sku(bearer: str, sku_id: int):
    """
    Takes a sku id and returns pricing data for that sku, only accepts one sku id at a time

    Endpoint name is Get Market Price by SKU

    :param bearer: string based access token
    :param sku_id: integer based single sku id
    :return: pricing data in the form of a json object with no error header
    """
    url = "https://api.tcgplayer.com/pricing/marketprices/{}".format(sku_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Request had an invalid group id and is either 0 or less than 0
    elif response.status_code == 400:
        raise InvalidSkuIdRequest()
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found for the group id or it was invalid
    elif response.status_code == 404:
        raise InvalidPricingRequest()
