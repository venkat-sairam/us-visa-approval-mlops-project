from typing import Optional
from src.configuration.mongo_connection import MongoDBClient
from src.constant import DATABASE_NAME
from src.exception import CustomException
from src.utils import pd
from src.utils import np


class Read_US_Visa_Data:

    def __init__(self):

        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e)

    def export_mongo_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            if database_name is None:
                self.collection = self.mongo_client.database[collection_name]
            else:
                self.collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(self.collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise CustomException(e)
