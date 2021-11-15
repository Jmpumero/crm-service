from typing import Optional


class GetAllQueryParams:
    def __init__(self, query: Optional[str] = None, skip: int = 0, limit: int = 25):
        self.query = query
        self.skip = skip
        self.limit = limit
