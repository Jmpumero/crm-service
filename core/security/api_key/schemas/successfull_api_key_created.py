from pydantic import BaseModel


class SuccessfullApiKeyCreated(BaseModel):
    message: str
    api_key: str
