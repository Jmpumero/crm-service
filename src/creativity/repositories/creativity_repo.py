from core.connection.connection import ConnectionMongo


class CreativityRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()
