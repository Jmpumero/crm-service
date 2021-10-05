from typing import Any, List, Optional
from pydantic import BaseModel


class Email(BaseModel):
    email: str
    subscribed: bool
    is_primary: Optional[bool]


class Device(BaseModel):
    mac_address: str
    subscribed: bool


class Phone(BaseModel):
    phone: str
    is_primary: Optional[bool]
    subscribed: bool


class CustomerMarketingSubscriptions(BaseModel):
    emails: List[Email]
    devices: List[Device]
    phones: List[Phone]
