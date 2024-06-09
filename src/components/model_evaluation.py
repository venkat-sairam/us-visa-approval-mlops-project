from src.constant import CURRENT_YEAR, TARGET_COLUMN
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
)
from src.entity.config_entity import ModelEvaluationConfig
from src.exception import CustomException
from src.utils import read_from_csv_file, sys
from src.entity.s3_estimator import USvisaEstimator
from sklearn.metrics import f1_score
from dataclasses import dataclass
from src.logger import logging


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
        model_evaluation_config: ModelEvaluationConfig,
    ) -> None:
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)

    def get_best_model(self):
        try:
            bucket_name = self.model_evaluation_config.bucket_name
            model_path = self.model_evaluation_config.s3_model_path
            estimator = USvisaEstimator(bucket_name=bucket_name, model_path=model_path)
            if estimator.is_model_present(model_path=model_path):
                return estimator
            return None
        except Exception as e:
            raise CustomException(e, sys)

    def evaluate_model(self):
        try:
            test_data = read_from_csv_file(
                file_path=self.data_ingestion_artifact.test_file_path
            )
            test_data["company_age"] = CURRENT_YEAR - test_data["yr_of_estab"]
            X, y = test_data.drop(TARGET_COLUMN, axis=1), test_data[TARGET_COLUMN]
            y = y.apply(lambda x: 1 if x == "Certified" else 0)
            trained_model_f1_score = self.model_trainer_artifact.model_metrics[
                "f1_score"
            ]

            best_model_f1_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_pred = best_model.predict(X)
                best_model_f1_score = f1_score(y_pred, y)
            tmp_best_model_score = (
                0 if best_model_f1_score is None else best_model_f1_score
            )
            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                difference=trained_model_f1_score - tmp_best_model_score,
            )
            logging.info(f"model evaluation result: {result}")
            return result

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self):
        try:
            model_evaluate_details = self.evaluate_model()
            s3_model_path = self.model_evaluation_config.s3_model_path

            model_evaluation_artifact_details = ModelEvaluationArtifact(
                is_evaluated=model_evaluate_details.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_file_path=model_evaluate_details.trained_model_f1_score,
                difference_in_accuracy=model_evaluate_details.difference,
            )
            logging.info(
                f"Model Evaluation Artifact details are: {model_evaluation_artifact_details}"
            )
            return model_evaluation_artifact_details
        except Exception as e:
            raise CustomException(e, sys)
