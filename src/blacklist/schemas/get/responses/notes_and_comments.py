from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel


class Link(BaseModel):
    href: str


class Links(BaseModel):
    self: Link
    clients: Link


class CustomerNotesAndcomments(BaseModel):
    date: str
    comment: str
    created_by: str
    belong: str


class NotesAndCommentsResponse(BaseModel):
    customer_comments: List[CustomerNotesAndcomments]
    #
    total_show: int
