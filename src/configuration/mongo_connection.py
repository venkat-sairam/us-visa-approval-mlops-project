from src.logger import logging
from src.constant import DATABASE_NAME
from src.exception import CustomException
from src.constant import os, MONGODB_URL_KEY
from pymongo.mongo_client import MongoClient


class MongoDBClient:
    """
    Description :   This method creates connection to given Mongo DB database
    Output      :   None
    On Failure  :   raises an 'MONGODB_URL_KEY is not specified' as exception message
    """

    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                # mongo_db_url = os.getenv("MONGODB_URL_KEY")
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception("MONGODB_URL_KEY is not specified")
                MongoDBClient.client = MongoClient(mongo_db_url)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("Mongo DB Connection established successfully...!")
        except Exception as e:
            raise CustomException(e)
