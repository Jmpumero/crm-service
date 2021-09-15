from typing import Optional
from pydantic import BaseModel


class ResponseMetaData(BaseModel):
    code: int
    message: str


class Link(BaseModel):
    href: str


class Links(BaseModel):
    self: Link
    clients: Link


class Client(BaseModel):
    id: Optional[int]
    name: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    organization: Optional[str]
    links: Optional[Links]
    isLead: Optional[bool]
    salesAgent: Optional[str]


class CreateClientResponse(BaseModel):
    response: ResponseMetaData
    #client: Optional[Client]
