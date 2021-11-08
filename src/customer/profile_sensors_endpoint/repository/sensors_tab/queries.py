from src.customer.repository import MongoQueries
from config.config import Settings


global_settings = Settings()


class SensorsTabQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def get_associated_sensors(self, customer_id):
        sensors = self.customer.find_one(
            {"_id": customer_id}, {"associated_sensors": 1}
        )
        return sensors
