from typing import Any, Coroutine

from core.connection.connection import ConnectionMongo


class SearchQueries(ConnectionMongo):
    def __init__(self) -> None:
        super().__init__()
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
            "associated_sensors": 1,
            "blacklist_status": 1,
            "blacklist_last_enabled_motive": 1,
            "blacklist_last_disabled_motive": 1,
            "customer_status": 1,
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
            "language_main": {
                "$arrayElemAt": [
                    "$languages",
                    {"$indexOfArray": ["$languages.isMain", True]},
                ]
            },
        }

    def build_search_match(self, item) -> dict:

        match = {"$match": {}}
        if item != None:
            match = {
                "$match": {
                    "$or": [
                        # {
                        #     "name": {
                        #         "$regex": f".*{item}.*",
                        #         "$options": "i",
                        #     }
                        # },
                        # {
                        #     "last_name": {
                        #         "$regex": f".*{item}.*",
                        #         "$options": "i",
                        #     }
                        # },
                        # {
                        #     "civil_status": {
                        #         "$regex": f".*{item}.*",
                        #         "$options": "i",
                        #     }
                        # },
                        {
                            "email": {
                                "$elemMatch": {
                                    "email": {
                                        "$regex": f".*{item}.*",
                                        "$options": "i",
                                    },
                                    "isMain": True,
                                }
                            }
                        },
                        {
                            "address_main.main": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "phone_main.intl_format": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "language_main.language": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "language_main.language": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "documentId.documentNumber": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                    ]
                }
            }

        return dict(match)

    def set_column_sort(self, column):
        result = "name"

        if column == "email":
            result = "email_main.email"
        if column == "address":
            result = "address_main.address"
        if column == "phone":
            result = "phone_main.phone"

        return result

    def find_customers(self, skip, limit, q, order_sort, column_sort):
        customers = None

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

            # if column_sort == "email":
            #     if order_sort.lower() == "desc":

            #         customers = self.customer.aggregate(
            #             [
            #                 {
            #                     "$facet": {
            #                         "items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$skip": skip},
            #                             {"$limit": limit},
            #                             {"$project": self.search_projections},
            #                             {
            #                                 "$sort": {
            #                                     "email.email": -1,
            #                                     "_id": 1,
            #                                 }
            #                             },
            #                         ],
            #                         "total_items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$count": "total"},
            #                         ],
            #                     }
            #                 }
            #             ]
            #         )
            #     else:
            #         customers = self.customer.aggregate(
            #             [
            #                 {
            #                     "$facet": {
            #                         "items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$skip": skip},
            #                             {"$limit": limit},
            #                             {"$project": self.search_projections},
            #                             {
            #                                 "$sort": {
            #                                     "email.email": 1,
            #                                     "_id": 1,
            #                                 }
            #                             },
            #                         ],
            #                         "total_items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$count": "total"},
            #                         ],
            #                     }
            #                 }
            #             ]
            #         )

            # elif column_sort:
            #     if order_sort.lower() == "desc":

            #         customers = self.customer.aggregate(
            #             [
            #                 {
            #                     "$facet": {
            #                         "items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$skip": skip},
            #                             {"$limit": limit},
            #                             {"$project": self.search_projections},
            #                             {
            #                                 "$sort": {
            #                                     f"{column_sort}": -1,
            #                                     "_id": 1,
            #                                 }
            #                             },
            #                         ],
            #                         "total_items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$count": "total"},
            #                         ],
            #                     }
            #                 }
            #             ]
            #         )
            #     else:

            #         customers = self.customer.aggregate(
            #             [
            #                 {
            #                     "$facet": {
            #                         "items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$skip": skip},
            #                             {"$limit": limit},
            #                             {"$project": search_projections},
            #                             {
            #                                 "$sort": {
            #                                     f"{column_order}": 1,
            #                                     "_id": 1,
            #                                 }
            #                             },
            #                         ],
            #                         "total_items": [
            #                             {"$match": {"customer_status": True}},
            #                             {"$count": "total"},
            #                         ],
            #                     }
            #                 }
            #             ]
            #         )
            # else:
            #     customers = self.customer.aggregate(
            #         [
            #             {
            #                 "$facet": {
            #                     "items": [
            #                         {"$match": {"customer_status": True}},
            #                         {"$skip": skip},
            #                         {"$limit": limit},
            #                         {"$project": search_projections},
            #                         {
            #                             "$sort": {
            #                                 f"{column_order}": 1,
            #                                 "_id": 1,
            #                             }
            #                         },
            #                     ],
            #                     "total_items": [
            #                         {"$match": {"customer_status": True}},
            #                         {"$count": "total"},
            #                     ],
            #                 }
            #             }
            #         ]
            #     )

        elif q != None and column_sort == None:

            match = self.build_search_match(q)

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
