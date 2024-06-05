from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])

DataIngestionConfig = namedtuple(
    "DataIngestionConfig",
    [
        "raw_data_dir",
        "ingested_dir",
        "ingested_train_dir",
        "ingested_test_dir",
        "collection_name",
        "train_test_split_ratio",
    ],
)


DataValidationConfig = namedtuple(
    "DataValidationConfig", ["report_dir", "drift_report_file_path"]
)


DataTransformationConfig = namedtuple(
    "DataTransformationConfig",
    [
        "transformed_directory",
        "transformed_train_file_path",
        "transformed_test_file_path",
        "preprocessed_directory",
        "preprocessed_object_file_path",
    ],
)
