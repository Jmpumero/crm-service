from os import name
from typing import Any, Coroutine

from core.connection.connection import ConnectionMongo


class SearchQueries(ConnectionMongo):
    def __init__(self) -> None:
        super().__init__()

        self.tb_without_img_pjt = {
            "name": 1,
            "last_name": 1,
            "age": 1,
            "email": 1,
            "phone": 1,
            "address": 1,
            "documentId": 1,
            "nationality": 1,
            "civil_status": 1,
            "languages": 1,
            "birthdate": 1,
            "customer_status": 1,
        }

        self.response_clear = {
            "name": 1,
            "last_name": 1,
            "age": 1,
            "email": 1,
            "phone": 1,
            "address": 1,
            "documentId": 1,
            "nationality": 1,
            "civil_status": 1,
            "birthdate": 1,
        }

    def build_sentence(self, q, field, sub_field=None):
        if sub_field:
            r = {
                f"{field}": {
                    "$elemMatch": {
                        f"{sub_field}": {
                            "$regex": f".*{q}.*",
                            "$options": "i",
                        },
                        "isMain": True,
                    }
                }
            }
        else:
            r = {
                f"{field}": {
                    "$regex": f".*{q}.*",
                    "$options": "i",
                }
            }

        return dict(r)

    def build_search_match(self, item) -> dict:

        match = {"$match": {}}

        if item != None:
            match = {
                "$match": {
                    "$or": [
                        self.build_sentence(item, "name", None),
                        self.build_sentence(item, "full_name", None),
                        self.build_sentence(item, "last_name", None),
                        self.build_sentence(item, "civil_status", None),
                        self.build_sentence(item, "email", "email"),
                        self.build_sentence(item, "address", "address"),
                        self.build_sentence(item, "phone", "intl_format"),
                        self.build_sentence(item, "languages", "language"),
                        self.build_sentence(item, "documentId", "documentNumber"),
                    ]
                }
            }

        return dict(match)

    def set_column_sort(self, column):
        result = column
        if column == "email":
            result = "email.email"
        elif column == "address":
            result = "address.address"
        elif column == "phone":
            result = "phone.intl_format"
        elif column == "languages":
            result = "languages.language"
        elif column == "documentId":
            result = "documentId.documentNumber"
        elif column == None or column == "":
            result = "name"
        return result

    def find_customers(self, skip, limit, q, order_sort, column_sort):
        customers = None
        order = 1
        if order_sort == "desc":
            order = -1

        if q == None and column_sort == None:  # show all

            customers = self.customer.aggregate(
                [
                    {
                        "$facet": {
                            "items": [
                                {"$match": {"customer_status": True}},
                                {"$skip": skip},
                                {"$limit": limit},
                                {"$project": self.tb_without_img_pjt},
                                # {"$project": self.response_clear},
                            ],
                            "total_items": [
                                {"$match": {"customer_status": True}},
                                {"$count": "total"},
                            ],
                            "total_items_show": [
                                {"$match": {"customer_status": True}},
                                {"$skip": skip},
                                {"$limit": limit},
                                {"$count": "total_show"},
                            ],
                        }
                    }
                ]
            )

        else:

            match = self.build_search_match(q)
            column = self.set_column_sort(column_sort)

            customers = self.customer.aggregate(
                [
                    {
                        "$facet": {
                            "items": [
                                {"$match": {"customer_status": True}},
                                match,
                                {"$skip": skip},
                                {"$limit": limit},
                                {"$project": self.tb_without_img_pjt},
                                # {"$project": self.response_clear},
                                {
                                    "$sort": {
                                        f"{column}": order,
                                        "_id": 1,
                                    }
                                },
                            ],
                            "total_items": [
                                {"$match": {"customer_status": True}},
                                match,
                                {"$count": "total"},
                            ],
                            "total_items_show": [
                                {"$match": {"customer_status": True}},
                                match,
                                {"$skip": skip},
                                {"$limit": limit},
                                {"$count": "total_show"},
                            ],
                        }
                    }
                ]
            )

        return customers
