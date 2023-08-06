from dataclasses import field
from typing import Generic, TypeVar

import marshmallow
from marshmallow_dataclass import dataclass

T = TypeVar("T")


@dataclass
class APIResponse(Generic[T]):
    success: bool
    errors: list[str]
    results: list[T]


@dataclass
class APIError():
    message: str
    messageDetail: str
