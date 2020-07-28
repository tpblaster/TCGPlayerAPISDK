import json

import requests

from errors import InvalidBearerToken, InvalidCategoryId, InvalidCategoryRequest, InvalidListLength, InvalidGroupId, \
    NoDataFoundForGroup, InvalidProductIdRequest, InvalidSkuIdRequest


def get_all_category_groups(bearer: str, category_id: int, offset: int = 0, limit: int = 10):
    """
    Takes a category id and returns possible groups, can be paged using offset

    Endpoint name is List All Category Groups

    :param bearer: string based access token
    :param category_id: integer based category id
    :param offset: optional offset from beginning of results
    :param limit: optional limit for the number of results returned, default to 10
    :return: returns json object of the results with no error object
    """
    url = "https://api.tcgplayer.com/catalog/categories/{}/groups?offset={}&limit={}".format(category_id, offset, limit)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Category id was 0 or less than oneSS
    elif response.status_code == 400:
        raise InvalidCategoryId()
    # Invalid bearer token, please create a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # No data was found for the category id or it was invalid
    elif response.status_code == 404:
        raise InvalidCategoryRequest()


# category name seems to be redundant as category id must be specified or the endpoint will return a 400 status code

def get_group_info_search(bearer: str, category_id: int, category_name: str = None, supplemental: bool = None,
                          has_sealed: bool = None, sort_order: str = None, sort_desc: bool = False, offset: int = 0,
                          limit: int = 10):
    """
    Takes more advanced query parameters and returns group data for a given category

    Endpoint name is List All Groups Details

    :param bearer: string based access token
    :param category_id: integer based category to used in the query
    :param category_name: optional string based category name to used in the query
    :param supplemental: boolean value to choose how supplemental sets are returned, defaults to None
    :param has_sealed: boolean value to chose if sets must have sealed product, defaults to None
    :param sort_order: string based value used to determine how the results are sorted default is name from the API backend
    :param sort_desc: boolean value to choose how values are used to sort, defaults to ascending if true then it will sort by descending
    :param offset: optional offset from the beginning of the result, can be used for paging and defaults to 0
    :param limit: number of results to be returned, defaults to 10 and can be used for paging
    :return: returns results as a json object with no error object data
    """
    url = "https://api.tcgplayer.com/catalog/groups"
    headers = {'Authorization': 'Bearer ' + bearer}
    payload = {
        'categoryId': category_id,
        'categoryName': category_name,
        'isSupplemental': supplemental,
        'hasSealed': has_sealed,
        'sortOrder': sort_order,
        'sortDesc': sort_desc,
        'offset': offset,
        'limit': limit
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Category id error
    elif response.status_code == 400:
        raise InvalidCategoryId()
    # Invalid bearer token, please create a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    elif response.status_code == 404:
        raise InvalidCategoryRequest()


def get_all_category_media(bearer: str, category_id: int):
    """
    Takes a category and returns category wide media like cardbacks

    Endpoint name is List All Category Media

    :param bearer: string based access token
    :param category_id: integer based category id
    :return: returns results in a json object
    """
    url = "https://api.tcgplayer.com/catalog/categories/{}/media".format(category_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Category id error
    elif response.status_code == 400:
        raise InvalidCategoryId()
    # Invalid bearer token, please create a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    elif response.status_code == 404:
        raise InvalidCategoryRequest()


def get_group_media(bearer: str, group_id: int):
    """
    Takes a group id and returns group wide media like set symbols

    Endpoint name is List All Group Media

    :param bearer: string based access token
    :param group_id: single integer based group id
    :return: returns results of json object with media data
    """
    url = "https://api.tcgplayer.com/catalog/groups/{}/media".format(group_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    elif response.status_code == 400:
        raise InvalidGroupId()
    # Invalid bearer token, please create a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    elif response.status_code == 404:
        raise NoDataFoundForGroup()


def get_group_details(bearer: str, group_ids: list):
    """
    Takes a list of group ids and returns information about each group

    Endpoint name is Get Group Details

    :param bearer: string based access token
    :param group_ids: list of group ids as integers to be queried
    :return: returns full json data with potential errors indicated in the object
    """
    # Handles potential 400 responses
    if len(group_ids) > 250 or len(group_ids) < 1:
        raise InvalidListLength(len(group_ids))
    url = "https://api.tcgplayer.com/catalog/groups/" + ','.join(map(str, group_ids))
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # All groups were found and data was returned
    if response.status_code == 200:
        return json.loads(response.text)
    # Some groups were found and returned, those that were not found are returned in the error section
    elif response.status_code == 207:
        return json.loads(response.text)
        # Invalid bearer token, please create a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    elif response.status_code == 404:
        raise InvalidCategoryRequest()


def get_list_all_products(bearer: str, category_id: int = None, category_name: str = None, group_id: int = None,
                          group_name: str = None, product_name: str = None, get_extended_fields: bool = False,
                          product_types: list = None, offset: int = 0, limit: int = 10, include_skus: bool = False):
    """
    Takes a series of parameters for potential products and returns product data, can be paged with offset and limit

    Endpoint name is List All Products

    :param bearer: string based access token
    :param category_id: optional integer based category to used in the query
    :param category_name: optional string based category name to used in the query
    :param group_id: optional integer based group id to used in the query
    :param group_name: optional group name to used in the query
    :param product_name: optional product name to used in the query
    :param get_extended_fields: boolean value to get extra data returned
    :param product_types: optional list of string based product types to used in the query
    :param offset: optional offset from the beginning of the result, can be used for paging and defaults to 0
    :param limit: number of results to be returned, defaults to 10 and can be used for paging
    :param include_skus: boolean value to include sku ids in the returned data for each product id
    :return: returns result of query as a json object
    """
    url = "https://api.tcgplayer.com/catalog/products"
    headers = {'Authorization': 'Bearer ' + bearer}
    payload = {
        'categoryId': category_id,
        'categoryName': category_name,
        'groupId': group_id,
        'groupName': group_name,
        'productName': product_name,
        'getExtendedFields': get_extended_fields,
        'productTypes': product_types,
        'offset': offset,
        'limit': limit,
        'includeSkus': include_skus
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    # Response was valid and results are returned
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    # Invalid bearer token was passed, generate a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters
    elif response.status_code == 404:
        raise InvalidCategoryRequest()


def get_product_details(bearer: str, product_ids: list, get_extended_fields: bool = False, include_skus: bool = False):
    """
    Takes a list of product ids as integers and returns info about each one

    Endpoint name is Get Product Details

    :param bearer: string based access token
    :param product_ids: list of product ids to get data for, should be integers
    :param get_extended_fields: boolean value used to get extra data
    :param include_skus: boolean valued used to get sku ids for each product id
    :return: returns full json data with potential error data in the object
    """
    # Handles potential 400 responses
    if len(product_ids) > 250 or len(product_ids) < 1:
        raise InvalidListLength(len(product_ids))
    url = "https://api.tcgplayer.com/catalog/products/" + ','.join(map(str, product_ids))
    headers = {'Authorization': 'Bearer ' + bearer}
    payload = {
        'getExtendedFields': get_extended_fields,
        'includeSkus': include_skus
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    # All product ids returned data
    if response.status_code == 200:
        return json.loads(response.text)
    # Some product ids returned data, those that didn't are returned in the error field
    elif response.status_code == 207:
        return json.loads(response.text)
    # Invalid bearer token was passed, generate a new one
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters or product ids
    elif response.status_code == 404:
        raise InvalidProductIdRequest()


def get_product_skus(bearer: str, product_id: int):
    """
    Takes a product id and returns all sku ids for that product

    Endpoint name is List Product SKUs

    :param bearer: string based access token
    :param product_id: integer based product id
    :return: results from json, no error data
    """
    url = "https://api.tcgplayer.com/catalog/products/{}/skus".format(product_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters or product ids
    elif response.status_code == 404:
        raise InvalidProductIdRequest()


def get_related_products(bearer: str, product_id: int, limit: int = 10, offset: int = 0):
    """
    Takes a product id and returns related products

    Endpoint name is List Related Products

    :param bearer: string based access token
    :param product_id: integer based product id
    :param limit: number of results to return, can be up to 100
    :param offset: offset from beginning of result, used for paging
    :return: json based data of products along with header info for paging
    """
    url = "https://api.tcgplayer.com/catalog/products/{}/productsalsopurchased".format(product_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    payload = {
        'limit': limit,
        'offset': offset
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    if response.status_code == 200:
        return json.loads(response.text)
    elif response.status_code == 400:
        raise InvalidProductIdRequest()
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters or product id
    elif response.status_code == 404:
        raise InvalidProductIdRequest()


def get_product_media(bearer: str, product_id: int):
    """
    Takes a single product id and returns product media

    Endpoint name is List All Product Media Types

    :param bearer: string based access token
    :param product_id: integer based product id
    :return: returns media like the front and or back of the card
    """
    url = "https://api.tcgplayer.com/catalog/products/{}/media".format(product_id)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    elif response.status_code == 400:
        raise InvalidProductIdRequest()
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters or product id
    elif response.status_code == 404:
        raise InvalidProductIdRequest()


def get_sku_details(bearer: str, sku_list: list):
    """
    Takes a list of skus and returns sku details

    Endpoint name is Get SKU details

    :param bearer: string based access token
    :param sku_list: takes a list of sku ids as integers
    :return: returns full json data with potential errors indicated in object
    """
    # Handles potential 400 responses
    if len(sku_list) > 250 or len(sku_list) < 1:
        raise InvalidListLength(len(sku_list))
    url = "https://api.tcgplayer.com/catalog/skus/" + ','.join(map(str, sku_list))
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    # Data for all sku ids is returned
    if response.status_code == 200:
        return json.loads(response.text)
    # Data for some sku ids is returned, sku ids that failed are indicated in the error section
    elif response.status_code == 207:
        return json.loads(response.text)
    elif response.status_code == 400:
        raise InvalidSkuIdRequest()
    elif response.status_code == 401:
        raise InvalidBearerToken()
    # Request was invalid, check the formatting of the incoming parameters or product id
    elif response.status_code == 404:
        raise InvalidSkuIdRequest()
