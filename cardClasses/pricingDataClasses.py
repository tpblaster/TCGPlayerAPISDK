# Potential use in the future but for now they will not be used
class SkuPricingData:
    def __init__(self, skuId, lowPrice, lowestShipping, lowestListingPrice, marketPrice, directLowPrice):
        self.skuId = skuId
        self.lowPrice = lowPrice
        self.lowestShipping = lowestShipping
        self.lowestListing = lowestListingPrice
        self.marketPrice = marketPrice
        self.directLowPrice = directLowPrice

    def create_from_dict(request_result: dict):
        price_object = SkuPricingData(request_result["skuId"], request_result["lowPrice"], request_result["lowestShipping"], request_result["lowestListingPrice"], request_result["marketPrice"], request_result["directLowPrice"])
        return price_object

    def create_from_list_dict(result_list: list):
        list_sku_pricing = []
        for i in result_list:
            list_sku_pricing.append(SkuPricingData.create_from_dict(i))
        return list_sku_pricing
