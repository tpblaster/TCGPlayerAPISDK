class InvalidBearerToken(Exception):
    """
    Exception raised for errors where the api does not accept the users bearer token

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="bearer token is invalid"):
        self.message = message
        super().__init__(self.message)


class InvalidListLength(Exception):
    """
    Exception raised for errors where the list that was passed was out of the range for the endpoint

    Attributes:
        message -- explanation of the error
        list_length -- the length of the list that was out of range
    """

    def __init__(self, list_length, message="length of the list is out of range for the endpoint"):
        self.list_length = list_length
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.list_length} -> {self.message}'


class InvalidBearerRequest(Exception):
    """
    Exception raised when a request for a new bearer token fails

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="the request for a bearer token failed, check to make sure your keys were correctly "
                               "input"):
        self.message = message
        super().__init__(self.message)


class InvalidPricingRequest(Exception):
    """
    Exception raised when either no data was found or all ids passed were invalid

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="No data was found for the ids passed or the ids were invalid"):
        self.message = message
        super().__init__(self.message)


class InvalidGroupId(Exception):
    """
    Exception raised when a request is returned with a status code of 400 from an endpoint, this signifies that the
    group id was equal to or less than 0

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="group id was equal to or less than 0"):
        self.message = message
        super().__init__(self.message)


class InvalidCategoryId(Exception):
    """
    Exception raised when a request is returned with a status code of 400 from an endpoint, this signifies that the
    category id was equal to or less than 0

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="category id was equal to or less than 0"):
        self.message = message
        super().__init__(self.message)


class NoDataFoundForGroup(Exception):
    """
    Exception raised when a 404 response is returned by an endpoint that requests a group id and returns data

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="group id is invalid or group has no pricing data"):
        self.message = message
        super().__init__(self.message)


class InvalidCategoryRequest(Exception):
    """
    Exception raised when a 404 response is returned by an endpoint that accepts categories and returns groups

    Attributes:
        message --- explanation of the error
    """

    def __init__(self, message="category is invalid or has no data"):
        self.message = message
        super().__init__(self.message)


class InvalidProductIdRequest(Exception):
    """
    Exception raised when a 404 request is returned from an endpoint that takes product ids and returns non pricing data

    Attributes:
        message --- explanation of the error
    """

    def __init__(self, message="one or more product ids are invalid or have no data associated with them"):
        self.message = message
        super().__init__(self.message)


class InvalidSkuIdRequest(Exception):
    """
    Exception raised when a 404 request is returned from an endpoint that takes sku ids and returns non pricing data

    Attributes:
        message --- explanation of the error
    """

    def __init__(self, message="one or more sku ids are invalid or have no data associated with them"):
        self.message = message
        super().__init__(self.message)
