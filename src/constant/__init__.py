from src.utils import os, get_environment_variables
from datetime import date
from src.utils import get_current_timestamp

ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "model.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)


CURRENT_TIME_STAMP = get_current_timestamp()

DATABASE_NAME = "us-visa-database"

# COLLECTION_NAME = "visa_data"

MONGODB_URL_KEY = get_environment_variables(variable_name="MONGODB_URL")

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year


FILE_NAME: str = "usvisadataset.csv"
TRAIN_FILE_NAME: str = "train_data.csv"
TEST_FILE_NAME: str = "test_data.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


AWS_ACCESS_KEY_ID_ENV_KEY = get_environment_variables("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ENV_KEY = get_environment_variables("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "us-east-2"


# Pipeline details:
TRAINING_PIPELINE_CONFIG_KEY: str = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY: str = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY: str = "artifact_dir"

# Data Ingestion related constant start with DATA_INGESTION VAR NAME
DATA_INGESTION_CONFIG_KEY: str = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR_KEY: str = "data_ingestion_artifact_dir"
DATA_INGESTION_RAW_DATA_DIR_KEY: str = "raw_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR_KEY: str = "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY: str = "ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY: str = "ingested_test_dir"
DATA_INGESTION_COLLECTION_NAME_KEY: str = "collection_name"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO_KEY: float = "train_test_split_ratio"

# DATA VALIDATION CONSTANTS
DATA_VALIDATION_CONFIG_KEY: str = "data_validation_config"
DATA_VALIDATION_ARTIFACTS_DIR_NAME_KEY: str = "data_validation_artifact_dir"
DATA_VALIDATION_REPORT_DIR_NAME_KEY: str = "report_dir"
DATA_VALIDATION_REPORT_FILE_NAME_KEY: str = "report_file_name"
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH_KEY: str = "drift_report_file_path"


# Data transformation constants
DATA_TRANSFORMATION_CONFIG_KEY: str = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR_KEY: str = "data_transformation_artifact_dir"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY: str = "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_KEY: str = "transformed_train_file_name"
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_KEY: str = "transformed_test_file_name"
DATA_TRANSFORMATION_PREPROCESSED_DIR_KEY: str = "preprocessed_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY: str = (
    "preprocessed_object_file_name"
)


# Model Training related variables
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"


# Model Evaluation related variables
MODEL_EVALUATION_CONFIG_KEY= "model_evaluation_config"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE = "changed_threshold_score"
MODEL_EVALUATION_BUCKET_NAME="bucket_name"
MODEL_EVALUATION_S3_MODEL_PATH = "s3_model_key_path"


# Model Pusher Constants
MODEL_PUSHER_CONFIG_KEY ="model_pusher_config"
MODEL_PUSHER_BUCKET_NAME="bucket_name"
MODEL_PUSHER_S3_MODEL_PATH = "s3_model_key_path"
