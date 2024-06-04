from src.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
)
from src.utils import read_yaml_file
from src.constant import *
from src.logger import logging


class Configuration:
    def __init__(
        self,
        config_file_path: str = CONFIG_FILE_PATH,
        current_time_stamp=CURRENT_TIME_STAMP,
    ) -> None:
        self.config_info = read_yaml_file(filename=config_file_path)
        self.time_stamp = current_time_stamp
        self.training_pipeline_config = self.get_training_pipeline_config()

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        self.training_pipeline_info = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
        pipeline_name = self.training_pipeline_info[TRAINING_PIPELINE_NAME_KEY]
        artifact_dir = self.training_pipeline_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
        artifact_directory_path = os.path.join(ROOT_DIR, pipeline_name, artifact_dir)
        logging.info(f"Artifact directory path is: {artifact_directory_path}")
        training_pipeline_configuration_details = TrainingPipelineConfig(
            artifact_dir=artifact_directory_path
        )
        for i, config_details in enumerate(training_pipeline_configuration_details):
            logging.info(f" {config_details}")
        # logging.info(
        #     f"Training pipeline configuration details: {training_pipeline_configuration_details}"
        # )
        return training_pipeline_configuration_details

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        self.artifact_dir = self.training_pipeline_config.artifact_dir
        self.data_ingestion_config = self.config_info[DATA_INGESTION_CONFIG_KEY]

        self.data_ingestion_artifact_dir_name = self.data_ingestion_config[
            DATA_INGESTION_ARTIFACT_DIR_KEY
        ]

        self.data_ingestion_artifact_path = os.path.join(
            self.artifact_dir,
            self.data_ingestion_artifact_dir_name,
            self.time_stamp,
        )
        raw_data_dir = os.path.join(
            self.data_ingestion_artifact_path,
            self.data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY],
        )
        ingested_directory = os.path.join(
            self.data_ingestion_artifact_path,
            self.data_ingestion_config[DATA_INGESTION_INGESTED_DATA_DIR_KEY],
        )

        ingested_training_directory = os.path.join(
            ingested_directory,
            self.data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY],
        )

        ingested_test_directory = os.path.join(
            ingested_directory,
            self.data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DIR_KEY],
        )

        mongo_collection_name = self.data_ingestion_config[
            DATA_INGESTION_COLLECTION_NAME_KEY
        ]

        train_test_split_ratio = self.data_ingestion_config[
            DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO_KEY
        ]

        data_ingestion_configuration_details = DataIngestionConfig(
            raw_data_dir=raw_data_dir,
            ingested_dir=ingested_directory,
            ingested_train_dir=ingested_training_directory,
            ingested_test_dir=ingested_test_directory,
            collection_name=mongo_collection_name,
            train_test_split_ratio=train_test_split_ratio,
        )

        logging.info(
            f"Data ingestion configuration details are: {data_ingestion_configuration_details._asdict()}"
        )

        return data_ingestion_configuration_details

    def get_data_validation_config(self) -> DataValidationConfig:
        artifact_dir = self.training_pipeline_config.artifact_dir
        self.data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

        data_validation_artifact_directory_name = self.data_validation_info[
            DATA_VALIDATION_ARTIFACTS_DIR_NAME_KEY
        ]
        data_validation_artifact_path = os.path.join(
            ROOT_DIR,
            artifact_dir,
            data_validation_artifact_directory_name,
            self.time_stamp,
        )
        report_directory = os.path.join(
            data_validation_artifact_path,
            self.data_validation_info[DATA_VALIDATION_REPORT_DIR_NAME_KEY],
        )
        drift_report_file_path = os.path.join(
            report_directory,
            self.data_validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY],
        )
        data_validation_configuration_information = DataValidationConfig(
            report_dir=report_directory, drift_report_file_path=drift_report_file_path
        )

        logging.info(
            f"Validation configuration details: {data_validation_configuration_information}"
        )
        return data_validation_configuration_information

    def get_data_transformation_config(self) -> DataTransformationConfig:
        artifact_dir = self.training_pipeline_config.artifact_dir
        self.data_transformation_config = self.config_info[
            DATA_TRANSFORMATION_CONFIG_KEY
        ]
        data_transformation_artifact_dir = os.path.join(
            ROOT_DIR,
            artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_ARTIFACT_DIR_KEY],
        )

        transformed_dir = os.path.join(
            data_transformation_artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
        )

        transformed_train_dir = os.path.join(
            transformed_dir,
            self.data_transformation_config[
                DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY
            ],
        )
        transformed_test_dir = os.path.join(
            transformed_dir,
            self.data_transformation_config[
                DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY
            ],
        )

        preprocessed_dir = os.path.join(
            data_transformation_artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_DIR_KEY],
        )

        preprocessed_file_path = os.path.join(
            preprocessed_dir,
            self.data_transformation_config[
                DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY
            ],
        )

        data_transformation_configuration_details = DataTransformationConfig(
            transformed_directory=transformed_dir,
            transformed_train_directory=transformed_train_dir,
            transformed_test_directory=transformed_test_dir,
            preprocessed_directory=preprocessed_dir,
            preprocessed_object_file_name=preprocessed_file_path,
        )

        logging.info(
            f"Data Transformation configuration details are: {data_transformation_configuration_details}"
        )

        return data_transformation_configuration_details
