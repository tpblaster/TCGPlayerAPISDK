import json

import requests


# This endpoint takes a product condition id or a list of them and returns market data for them
# if you want pricing data for a single id then then use single_sku_market_price
# you can pass up to 250 sku ids into this endpoint
def list_sku_market_price(bearer, sku_list: list):
    if len(sku_list) > 250:
        return None
    url = "https://api.tcgplayer.com/pricing/sku/" + ','.join(sku_list)
    headers = {'Authorization': 'Bearer ' + bearer}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)["results"]
    else:
        return None
