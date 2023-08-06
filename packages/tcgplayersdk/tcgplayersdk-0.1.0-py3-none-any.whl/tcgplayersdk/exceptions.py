from marshmallow.exceptions import ValidationError
from requests import Response

from tcgplayersdk.schemas.api_response import APIError


class TCGPlayerSDKException(Exception):
    def __init__(self, response: Response):
        self.response = response
        try:
            self.error = APIError.Schema().loads(response.text)
        except ValidationError as e:
            self.error = None

    def __str__(self):
        if self.error is None:
            return self.response.text
        else:
            return self.error.messageDetail

    def __repr__(self):
        return repr(self.response)
