from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.configuration import Configuration
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
)
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from src.exception import CustomException
from src.utils import sys
from src.configuration import Configuration


class TrainPipeline:

    def __init__(self, configuration=Configuration()):
        try:
            self.config = configuration
        except Exception as e:
            raise CustomException(e)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:

            logging.info("started the data ingestion from training pipeline.....")
            data_ingestion = DataIngestion(self.config.get_data_ingestion_config())
            self.data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("data ingestion completed successfully...")

        except Exception as e:
            raise CustomException(e)

    def start_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("started the data validation from training pipeline.....")
            data_validation = DataValidation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_config=self.config.get_data_validation_config(),
            )
            self.data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("data validation completed successfully...")
        except Exception as e:
            raise CustomException(e)

    def start_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation...")
            data_transformation = DataTransformation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_artifact=self.data_validation_artifact,
                data_transformation_config=self.config.get_data_transformation_config(),
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformations()
            )
            logging.info("Data transformation completed successfully...!")
        except Exception as e:
            raise CustomException(e, sys)
