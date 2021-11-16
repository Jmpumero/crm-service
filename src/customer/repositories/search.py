from typing import Any, Coroutine


class SearchQueries:
    def __init__(self) -> None:

        self.search_projections = {
            "name": 1,
            "last_name": 1,
            "full_name": 1,
            "age": 1,
            "nationality": 1,
            "civil_status": 1,
            "documentId": 1,
            "booking_id": 1,
            "phone": {
                "$arrayElemAt": [
                    "$phone",
                    {"$indexOfArray": ["$phone.isMain", True]},
                ]
            },
            "email": {
                "$arrayElemAt": [
                    "$email",
                    {"$indexOfArray": ["$email.isMain", True]},
                ]
            },
            "address": {
                "$arrayElemAt": [
                    "$address",
                    {"$indexOfArray": ["$address.isMain", True]},
                ]
            },
        }

        self.blacklist_customer_projections = {
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
            "associated_sensors": 1,
            "blacklist_status": 1,
            "blacklist_last_enabled_motive": 1,
            "blacklist_last_disabled_motive": 1,
            "customer_status": 1,
            "customer_avatar": 1,
            "email_main": {
                "$arrayElemAt": [
                    "$email",
                    {"$indexOfArray": ["$email.isMain", True]},
                ]
            },
            "phone_main": {
                "$arrayElemAt": [
                    "$phone",
                    {"$indexOfArray": ["$phone.isMain", True]},
                ]
            },
            "address_main": {
                "$arrayElemAt": [
                    "$address",
                    {"$indexOfArray": ["$address.isMain", True]},
                ]
            },
        }

    def find_customers(self, skip, limit, q, order_sort, column_sort):

        if q == None and column_sort == None:

            customers = self.customer.aggregate(
                [
                    {
                        "$facet": {
                            "items": [
                                {"$match": {"customer_status": True}},
                                {"$skip": skip},
                                {"$limit": limit},
                                {"$project": self.search_projections},
                            ],
                            "total_items": [
                                {"$match": {"customer_status": True}},
                                {"$count": "total"},
                            ],
                        }
                    }
                ]
            )

            if column_sort == "email":
                if order_sort.lower() == "desc":

                    customers = self.customer.aggregate(
                        [
                            {
                                "$facet": {
                                    "items": [
                                        {"$match": {"customer_status": True}},
                                        {"$skip": skip},
                                        {"$limit": limit},
                                        {"$project": self.search_projections},
                                        {
                                            "$sort": {
                                                "email.email": -1,
                                                "_id": 1,
                                            }
                                        },
                                    ],
                                    "total_items": [
                                        {"$match": {"customer_status": True}},
                                        {"$count": "total"},
                                    ],
                                }
                            }
                        ]
                    )
                else:
                    customers = self.customer.aggregate(
                        [
                            {
                                "$facet": {
                                    "items": [
                                        {"$match": {"customer_status": True}},
                                        {"$skip": skip},
                                        {"$limit": limit},
                                        {"$project": self.search_projections},
                                        {
                                            "$sort": {
                                                "email.email": 1,
                                                "_id": 1,
                                            }
                                        },
                                    ],
                                    "total_items": [
                                        {"$match": {"customer_status": True}},
                                        {"$count": "total"},
                                    ],
                                }
                            }
                        ]
                    )

            elif column_order:
                if order.lower() == "desc":

                    customers = self.customer.aggregate(
                        [
                            {
                                "$facet": {
                                    "items": [
                                        {"$match": {"customer_status": True}},
                                        {"$skip": skip},
                                        {"$limit": limit},
                                        {"$project": search_projections},
                                        {
                                            "$sort": {
                                                f"{column_order}": -1,
                                                "_id": 1,
                                            }
                                        },
                                    ],
                                    "total_items": [
                                        {"$match": {"customer_status": True}},
                                        {"$count": "total"},
                                    ],
                                }
                            }
                        ]
                    )
                else:

                    customers = self.customer.aggregate(
                        [
                            {
                                "$facet": {
                                    "items": [
                                        {"$match": {"customer_status": True}},
                                        {"$skip": skip},
                                        {"$limit": limit},
                                        {"$project": search_projections},
                                        {
                                            "$sort": {
                                                f"{column_order}": 1,
                                                "_id": 1,
                                            }
                                        },
                                    ],
                                    "total_items": [
                                        {"$match": {"customer_status": True}},
                                        {"$count": "total"},
                                    ],
                                }
                            }
                        ]
                    )
            else:
                customers = self.customer.aggregate(
                    [
                        {
                            "$facet": {
                                "items": [
                                    {"$match": {"customer_status": True}},
                                    {"$skip": skip},
                                    {"$limit": limit},
                                    {"$project": search_projections},
                                    {
                                        "$sort": {
                                            f"{column_order}": 1,
                                            "_id": 1,
                                        }
                                    },
                                ],
                                "total_items": [
                                    {"$match": {"customer_status": True}},
                                    {"$count": "total"},
                                ],
                            }
                        }
                    ]
                )
        elif q != None and column_sort == None:
            ...
        return customers
