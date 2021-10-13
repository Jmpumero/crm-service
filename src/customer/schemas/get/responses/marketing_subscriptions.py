from typing import Any, List, Optional
from pydantic import BaseModel


class Email(BaseModel):
    email: Optional[str]
    subscribed: Optional[bool]
    is_primary: Optional[bool]


class Device(BaseModel):
    mac_address: Optional[str]
    subscribed: bool


class Phone(BaseModel):
    phone: Optional[str]
    is_primary: Optional[bool]
    subscribed: Optional[bool]


class CustomerMarketingSubscriptions(BaseModel):
    emails: Optional[List[Email]]
    devices: Optional[List[Device]]
    phones: Optional[List[Phone]]
