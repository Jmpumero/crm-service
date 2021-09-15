from pydantic import BaseModel


class SearchCustomersResponse(BaseModel):
    _id: str
    name: str
    last_name: str
    age: int
    email: str
    phone: str
    nationality: str
    address: str
    document_identification: str
    civl_status: str
