from src.constant import FILE_NAME, TRAIN_FILE_NAME, TEST_FILE_NAME
from src.logger import logging
from src.configuration.mongo_connection import MongoDBClient
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomException
from src.data_access.read_mongo_data import Read_US_Visa_Data
from src.utils import os
from sklearn.model_selection import train_test_split
from src.utils import pd


class DataIngestion:

    def __init__(
        self, data_ingestion_config: DataIngestionConfig
    ) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e)

    def export_data_into_raw_data_directory(self) -> pd.DataFrame:
        logging.info(f"Inside the export data definition....")
        try:
            connection = MongoDBClient()
            self.client = connection.client
            self.collection_name = self.data_ingestion_config.collection_name
            read_class = Read_US_Visa_Data()
            df = read_class.export_mongo_collection_as_dataframe(
                collection_name=self.collection_name
            )
            logging.info(f"Data Frame shape: {df.shape}")

            dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(dir, exist_ok=True)
            file_path = os.path.join(dir, FILE_NAME)

            df.to_csv(file_path, index=False, header=True)
            logging.info(f"Exported data frame into: {file_path}")
            return df
        except Exception as e:
            raise CustomException(e)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:

            """
            Method Name :   split_data_as_train_test
            Description :   This method splits the dataframe into train set and test set based on split ratio
            """
            logging.info("Inside the split_data_as_train_test method...")
            training_data, testing_data = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info(
                "Created Training data and testing data from original dataframe...."
            )
            ingested_directory = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_directory, exist_ok=True)
            # print(f"created ingested directory.... {'*'*25}")
            ingested_training_directory = self.data_ingestion_config.ingested_train_dir
            ingested_testing_directory = self.data_ingestion_config.ingested_test_dir

            os.makedirs(ingested_training_directory, exist_ok=True)
            os.makedirs(ingested_testing_directory, exist_ok=True)
            # print(f"created train/test directory.... {'*'*25}")
            train_file_path = os.path.join(ingested_training_directory, TRAIN_FILE_NAME)
            test_file_path = os.path.join(ingested_testing_directory, TEST_FILE_NAME)

            training_data.to_csv(train_file_path, index=False, header=True)
            testing_data.to_csv(test_file_path, index=False, header=True)

            logging.info("Training data and testing data exported successfully.....")
            return train_file_path, test_file_path
        except Exception as e:
            raise CustomException(e)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Inside the initiate data ingestion function.....")
        try:
            dataframe = self.export_data_into_raw_data_directory()
            train_file_path, test_file_path = self.split_data_as_train_test(
                dataframe=dataframe
            )
            logging.info("Exited from train and test split function...")

            data_ingestion_artifact_details = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
            )
            logging.info(
                f"Data Ingestion artifact details are: {data_ingestion_artifact_details}"
            )
            return data_ingestion_artifact_details
        except Exception as e:
            raise CustomException(e)
