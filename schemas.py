from math import dist
from typing import List
import datetime as _dt
from  pydantic import BaseModel


class _AddressBase(BaseModel):
    address: str
    coordinates: str



class AddressCreate(_AddressBase):
    pass


class _Address_dist_Base(BaseModel):
    coordinates: str
    distance: float

class AddressWithDistance(_Address_dist_Base):
    pass


class Address(_AddressBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _UserBase(BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Address] = []

    class Config:
        orm_mode = True