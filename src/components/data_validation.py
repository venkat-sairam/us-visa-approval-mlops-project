import json
from src.logger import logging
from src.constant import DATA_VALIDATION_DRIFT_REPORT_FILE_PATH_KEY, SCHEMA_FILE_PATH
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.exception import CustomException
from src.utils import read_from_csv_file, read_yaml_file, sys, pd, write_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:

            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.data_validation_schema_file = read_yaml_file(filename=SCHEMA_FILE_PATH)

        except Exception as e:
            raise CustomException(e, sys)

    def validate_columns_count(self, dataframe: pd.DataFrame) -> bool:

        try:
            status = len(dataframe.columns) == len(
                self.data_validation_schema_file["columns"]
            )
            logging.info(f"Does required columns exists in the dataframe ? {status}")
            return status
        except Exception as e:
            raise CustomException(e, sys)

    def validate_numerical_categorical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            original_data_columns = dataframe.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self.data_validation_schema_file["numerical_columns"]:
                if column not in original_data_columns:
                    missing_numerical_columns.append(column)

            for column in self.data_validation_schema_file["categorical_columns"]:
                if column not in original_data_columns:
                    missing_categorical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.info(
                    f"missing numerical columns in the dataframe are: {missing_numerical_columns}"
                )
            logging.info(f"All numerical columns are present in the dataframe")
            if len(missing_categorical_columns) > 0:
                logging.info(
                    f"missing categorical columns in the dataframe are: {missing_categorical_columns}"
                )
            logging.info(f"All categorical columns are present in the dataframe...")

            return (
                False
                if len(missing_numerical_columns) > 0
                or len(missing_categorical_columns) > 0
                else True
            )
        except Exception as e:
            raise CustomException(e, sys)

    def check_data_drift(
        self, reference_dataframe: pd.DataFrame, current_dataframe: pd.DataFrame
    ) -> bool:
        try:
            logging.info("Inside the check_data_drift function..")
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            logging.info(
                "Calculating the drift between the current dataframe and the target dataframe.."
            )
            data_drift_profile.calculate(reference_dataframe, current_dataframe)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            logging.info("writing the drift profile report to yaml file:")
            yaml_file_path = self.data_validation_config.drift_report_file_path

            write_yaml_file(
                file_path=yaml_file_path,
                content=json_report,
            )
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            logging.info(f"{n_drifted_features}/{n_features} drift detected")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status
        except Exception as e:
            raise CustomException(e, sys)

    def print_columns_count_validation_details(
        self, dataframe: pd.DataFrame, is_training_dataframe: bool = True
    ):
        logging.info("validating the column count in the given dataframe")
        validation_error_message = ""
        status = self.validate_columns_count(dataframe=dataframe)

        if not status:
            if is_training_dataframe:
                validation_error_message += "columns are missing in training data"
                logging.info("columns are missing in training data")
            else:
                validation_error_message += "columns are missing in testing data"
                logging.info("columns are missing in testing data")
        return status

    def print_column_types_validation_details(
        self, dataframe: pd.DataFrame, is_training_dataframe: bool = True
    ):
        logging.info("validating the column types in the given dataframe")
        validation_error_message = ""
        status = self.validate_numerical_categorical_columns(dataframe=dataframe)

        if not status:
            if is_training_dataframe:
                validation_error_message += "columns are missing in training data"
                logging.info("columns are missing in training data")
            else:
                validation_error_message += "columns are missing in testing data"
                logging.info("columns are missing in testing data")
        return status

    def initiate_data_validation(self) -> DataValidationConfig:
        try:
            logging.info("starting data validation")
            training_dataframe, testing_dataframe = (
                read_from_csv_file(
                    file_path=self.data_ingestion_artifact.train_file_path
                ),
                read_from_csv_file(
                    file_path=self.data_ingestion_artifact.test_file_path
                ),
            )
            status = self.print_columns_count_validation_details(training_dataframe)
            status = self.print_columns_count_validation_details(
                testing_dataframe, is_training_dataframe=False
            )
            status = self.print_column_types_validation_details(training_dataframe)
            status = self.print_column_types_validation_details(
                testing_dataframe, is_training_dataframe=False
            )
            validation_status = status
            if validation_status:

                drift_status = self.check_data_drift(
                    reference_dataframe=training_dataframe,
                    current_dataframe=testing_dataframe,
                )
                if drift_status:
                    logging.info("Drift detected..")
                else:
                    logging.info("Drift not detected")

            data_Validation_artifact_details = DataValidationArtifact(
                validation_status=validation_status,
                message="drift detected" if drift_status else "drift not detected",
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(
                f"Data Validation artifact details are: {data_Validation_artifact_details}"
            )
            return data_Validation_artifact_details
        except Exception as e:
            raise CustomException(e, sys)
