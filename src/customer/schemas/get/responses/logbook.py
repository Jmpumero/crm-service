from typing import Any

from pydantic import BaseModel


class CustomerLogBook(BaseModel):
    first_contact_info: Any
    another_contacts: Any
    total_items: Any
    items_shown: Any
