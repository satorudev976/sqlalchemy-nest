from typing import Optional
from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    id: int


class Item(ItemBase):
    id: int
    owner_id: int

    # Valid config keys have changed in pydantic V2
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    # Add items (create items by sqlalchemy-nest)
    items: list[ItemCreate] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@example.com",
                    "password": "password",
                    "items": [
                        {
                            "title": "title",
                            "description": "description"
                        }
                    ]
                }
            ]
        }
    }


class UserUpdate(UserBase):
    is_active: bool = True
    # Add items (update items by sqlalchemy-nest)
    items: list[ItemUpdate] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@example.com",
                    "is_active": True,
                    "items": [
                        {
                            "id": 1,
                            "title": "update_title",
                            "description": "update_description"
                        }
                    ]
                }
            ]
        }
    }


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    # Valid config keys have changed in pydantic V2
    model_config = ConfigDict(from_attributes=True)
