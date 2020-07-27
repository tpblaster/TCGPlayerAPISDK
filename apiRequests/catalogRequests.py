import json

import requests

from errors import InvalidBearerToken, InvalidCategoryId, InvalidCategoryRequest, InvalidListLength, InvalidGroupId, \
    NoDataFoundForGroup, InvalidProductIdRequest


# Takes a category id and returns possible groups, can be paged using offset
# Defaults are MTG as the category, offset of 0, and a result limit of 10

def get_all_category_groups(bearer: str, offset=0, limit=10, category_id=1):
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


# takes a more advanced query data and returns group data for a given category
# category name seems to be redundant as category id must be specified or the endpoint will return a 400 status code

def get_group_info_search(bearer: str, category_id: int, category_name: str = None, supplemental: bool = None,
                          has_sealed: bool = None, sort_order: str = None, sort_desc: bool = False, offset: int = 0,
                          limit: int = 10):
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


# Takes a category and returns category wide media like cardbacks

def get_all_category_media(bearer: str, category_id: int):
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


# Takes a list of group ids and returns information about each group, please pass a list of ints

def get_group_details(bearer: str, group_ids: list):
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


# Takes a series of parameters for potential products and returns product data, can be paged with offset and limit

def get_list_all_products(bearer: str, category_id: int = None, category_name: str = None, group_id: int = None,
                          group_name: str = None, product_name: str = None, get_extended_fields: bool = False,
                          product_types: list = None, offset: int = 0, limit: int = 10, include_skus: bool = False):
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


# Takes a list of product ids as integers and returns info about each one

def get_product_details(bearer: str, product_ids: list, get_extended_fields: bool = False, include_skus: bool = False):
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


# Takes a product id and returns all skus for that product
def get_product_skus(bearer: str, product_id: int):
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


# Takes a product id and returns related products, limit can be as high as 100
# can be paged using totalItems, offset and limit

def get_related_products(bearer: str, product_id: int, limit: int = 10, offset: int = 0):
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