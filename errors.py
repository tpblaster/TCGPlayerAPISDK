class invalid_bearer_token(Exception):
    """
    Exception raised for errors where the api does not accept the users bearer token

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="bearer token is invalid"):
        self.message = message
        super().__init__(self.message)
