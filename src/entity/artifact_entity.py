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

ModelTrainerArtifact = namedtuple(
    "ModelTrainerArtifact",
    [
        "is_trained",
        "message",
        "trained_model_file_path",
        "model_metrics",
    ],
)


ModelEvaluationArtifact = namedtuple(
    "ModelEvaluationArtifact",
    [
        "is_evaluated",
        "s3_model_path",
        "trained_model_file_path",
        "difference_in_accuracy",
    ],
)
