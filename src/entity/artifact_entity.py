from collections import namedtuple


DataIngestionArtifact = namedtuple(
    "DataIngestionArtifact", ["train_file_path", "test_file_path"]
)


DataValidationArtifact = namedtuple(
    "DataValidationArtifact", ["validation_status", "message", "drift_report_file_path"]
)


DataTransformationArtifact = namedtuple(
    "DataTransformationArtifact",
    [
        "transformed_object_file_path",
        "transformed_training_file_path",
        "transformed_test_file_path",
    ],
)
