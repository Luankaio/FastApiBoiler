from pymongo import MongoClient

class DataBaseConnection:
    def __init__(self, uri: str, database_name: str):
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        if self.client is None:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            self.client = None