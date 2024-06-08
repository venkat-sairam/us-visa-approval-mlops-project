from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.components.model_trainer import ModelTrainer
from src.configuration import Configuration
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact,
)
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from src.exception import CustomException


def print_before_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{'>>'*12} Executing function: {func.__name__}  {'<<' * 12}")
        result = func(*args, **kwargs)
        logging.info(
            f"{'>>'*12} Finished executing function: {func.__name__}  {'<<' * 12}"
        )
        return result

    return wrapper


class TrainPipeline:

    def __init__(self, configuration=Configuration()):
        try:
            self.config = configuration
        except Exception as e:
            raise CustomException(e)

    @print_before_execution
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Started the data ingestion from training pipeline...")
            data_ingestion = DataIngestion(self.config.get_data_ingestion_config())
            self.data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully...")
            return self.data_ingestion_artifact
        except Exception as e:
            raise CustomException(e)

    @print_before_execution
    def start_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Started the data validation from training pipeline...")
            data_validation = DataValidation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_config=self.config.get_data_validation_config(),
            )
            self.data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully...")
            return self.data_validation_artifact
        except Exception as e:
            raise CustomException(e)

    @print_before_execution
    def start_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation...")
            data_transformation = DataTransformation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_artifact=self.data_validation_artifact,
                data_transformation_config=self.config.get_data_transformation_config(),
            )
            self.data_transformation_artifact = (
                data_transformation.initiate_data_transformations()
            )
            logging.info("Data transformation completed successfully!")
            return self.data_transformation_artifact
        except Exception as e:
            raise CustomException(e)

    @print_before_execution
    def start_model_training(self):
        try:
            logging.info("Starting model training...")
            print(f"{'*' * 25} Data transformation details are: {'*' * 25}")
            print(self.data_transformation_artifact)
            model_trainer = ModelTrainer(
                data_transformation_artifact=self.data_transformation_artifact,
                model_trainer_config=self.config.get_model_trainer_config(),
            )
            logging.info(f"{'>>' * 10} Model trainer details are: {'<<' * 10}")
            self.model_trainer_artifact = model_trainer._initiate_model_trainer()
            logging.info("Model training completed...")
            return self.model_trainer_artifact
        except Exception as e:
            raise CustomException(e)
