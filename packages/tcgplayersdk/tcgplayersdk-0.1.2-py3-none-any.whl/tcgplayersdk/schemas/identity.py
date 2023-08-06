from datetime import datetime, timezone

from dateutil import parser
from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass(base_schema=SnakeCaseSchema)
class Identity():
    access_token: str
    token_type: str
    expires_in: int
    user_name: str
    issued: datetime
    expires: datetime

    # TODO: This can be a fancier serialization method
    @classmethod
    def from_json(cls, data):
        return cls(
            access_token=data['access_token'],
            token_type=data['token_type'],
            expires_in=data['expires_in'],
            user_name=data['userName'],
            issued=parser.parse(data['.issued']),
            expires=parser.parse(data['.expires']),
        )

    def is_expired(self) -> bool:
        return self.expires is None or datetime.now(timezone.utc) > self.expires
