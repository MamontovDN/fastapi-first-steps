from enum import Enum
from typing import Optional, Set
from pydantic import BaseModel, HttpUrl, Field, EmailStr


class Post(BaseModel):
    name: str
    text: str
    cost: int
    feed: Optional[float]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class UserDB(BaseModel):
    username: str
    hash_password: str
    email: EmailStr
    full_name: Optional[str]


class UserIn(BaseModel):
    username: str = Field(
        ...,
        title="Your login",
        example="loki69",
        max_length=50
    )
    password: str = Field(
        ...,
        title="Your password",
        example="qwerty1234",
        max_length=50
    )
    email: EmailStr
    full_name: Optional[str] = Field(
        None,
        title="Your Full Name",
        example="Loki Utunhaim",
        max_length=150,
    )


class UserOut(BaseModel):
    username: str = Field(
        ...,
        title="Your login",
        example="loki69",
        max_length=50
    )
    email: EmailStr
    full_name: Optional[str] = Field(
        None,
        title="Your Full Name",
        example="Loki Utunhaim",
        max_length=150,
    )


class Item(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = Field(
        None,
        title="description for item",
        max_length=300,
    )
    price: float = Field(
        None,
        ge=1,
        title="Price for Post",
        description="You pay 90% of cost to Author"
    )
    tax: Optional[float] = None
    co_founders: Set[UserOut] = Field(
        [],
        title="Co founders of the post",
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "url": "127.0.0.1/posts",
                "description": "post description",
                "price": 100.0,
                "tax": 1.1,
                "co_founders": [
                    {'username': "david123", 'full_name': "David Lubovsky"},
                    {'username': "alogo", 'full_name': "Alter Ogov"},
                ]
            }
        }