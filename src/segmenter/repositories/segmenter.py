from os import sync
from typing import Any

from pymongo import ReturnDocument
from datetime import datetime

from ..schemas import UpdatedSegment, FilterSegment
from core.connection.connection import ConnectionMongo

from .demography_querys import DemographyRepo


class SegmenterDetailsRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()
        self.demography = DemographyRepo()

    async def create_segment(self, data: dict[str, str]) -> Any:
        new_segment: Any = await self.segments.insert_one(data)

        return new_segment

    async def find_one_segment(self, id):

        return await self.segments.find_one({"_id": id})

    async def find_one_and_update(
        self, segment_id: str, updated_segment: UpdatedSegment
    ) -> Any:
        body_update = self.demography.convert_date_update(updated_segment.dict())
        # print(body_update)
        pipeline = self.build_pipeline_segment(body_update)
        segment: Any = await self.segments.find_one_and_update(
            {"_id": segment_id},
            {"$set": body_update},
            return_document=ReturnDocument.AFTER,
        )

        return segment

    async def find_and_update_status(self, segment_id, status):

        return await self.segments.find_one_and_update(
            {"_id": segment_id},
            {"$set": {"status": status}},
        )

    def set_stages_date(self, status, data):
        aggregation_array = []
        project_date = self.demography.builder_date_query_project()
        # ******
        from_ = datetime.fromtimestamp(data["date_range"]["from_"] / 1000)
        to = datetime.fromtimestamp(data["date_range"]["to"] / 1000)
        # *****
        date_range = self.demography.builder_date_range(
            status,
            "create_at",
            "Between",
            "",
            from_,
            to,
        )
        # *******
        aggregation_array.append({"$match": {"birthdate": {"$not": {"$eq": ""}}}})
        aggregation_array.append(project_date)
        # *************************
        aggregation_array.append(date_range)

        return aggregation_array

    def build_basic_demography_stages(self, filter, array, key, status):

        if filter[f"{key}"] != "" and filter[f"{key}"] != None:
            array.append(
                self.demography.builder_generic_query(
                    f"{key}", filter[f"{key}"], status
                )
            )
        return array

    def set_stages_demography(self, array, status, data):
        array_filters = data["applied_filters"]

        for filter in array_filters:
            if filter["filter_name"] == "demography":

                # array = self.build_basic_demography_stages(
                #     filter, array, "gender", status
                # )
                # array = self.build_basic_demography_stages(
                #     filter, array, "civil_status", status
                # )
                # array = self.build_basic_demography_stages(
                #     filter, array, "profession", status
                # )
                # array = self.build_basic_demography_stages(
                #     filter, array, "nationality", status
                # )
                # array = self.build_basic_demography_stages(
                #     filter, array, "childrens", status
                # )

                # if filter["age_range"] != None and filter["age_range"] != "":

                #     array.append(
                #         self.demography.builder_age_range(
                #             status,
                #             filter["age_range"]["from_"],
                #             filter["age_range"]["to"],
                #         )
                #     )

                if (
                    filter["birth_date"] != None
                    and filter["birth_date"]["condition"] != "Between"
                    and filter["birth_date"]["date"] != None
                ):
                    print("Dios no me he muerto, porque me quieres o porque me odias?")
                    date = self.demography.milliseconds_to_date(
                        int(filter["birth_date"]["date"])
                    )

                    array.append(
                        self.demography.builder_date_range(
                            status,
                            "birthdate",
                            filter["birth_date"]["condition"],
                            date,
                            "",
                            "",
                        )
                    )
                elif (
                    filter["birth_date"] != None
                    and filter["birth_date"]["condition"] == "Between"
                ):
                    print("***************")
                    from_ = self.demography.milliseconds_to_date(
                        int(filter["birth_date"]["date_range"]["from_"])
                    )
                    to = self.demography.milliseconds_to_date(
                        int(filter["birth_date"]["date_range"]["to"])
                    )
                    array.append(
                        self.demography.builder_date_range(
                            status,
                            "birthdate",
                            "Between",
                            "",
                            from_,
                            to,
                        )
                    )

                # if filter["languages"] != None:

                #     array.append(
                #         self.demography.builder_language("all", filter["languages"])
                #     )
                ...
        return array

    def build_pipeline_segment(self, data: dict) -> Any:

        aggregation_array = []
        aggregation_array = self.set_stages_date(True, data)
        aggregation_array = self.set_stages_demography(aggregation_array, True, data)
        print(aggregation_array)
        aggregation_array.append({"$count": "total"})
        r = self.customer.aggregate(aggregation_array)

        return r

    async def apply_filter_segment(self, data: dict) -> Any:

        t = None
        t = self.build_pipeline_segment(data)

        r = await t.to_list(length=None)

        return r
