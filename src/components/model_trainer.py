from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.exception import CustomException
from src.utils import load_object, sys, load_numpy_array_data, np, save_object
from src.logger import logging
from neuro_mf import ModelFactory
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from src.entity.estimator import PredictModel


class ModelTrainer:

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ) -> None:
        try:
          
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e, sys)

    def get_model_object_and__metrics(
        self, train_array: np.array, test_array: np.array
    ):

        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(
                model_config_path=self.model_trainer_config.model_config_file_path
            )

            logging.info(
                "Splitting the train/test arrays into input and target features..."
            )
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            best_model_details = model_factory.get_best_model(
                X=x_train,
                y=y_train,
                base_accuracy=self.model_trainer_config.base_accuracy,
            )
            logging.info(f"Best model found on training dataset: {best_model_details}")
            model_obj = best_model_details.best_model

            y_pred = model_obj.predict(x_test)
            accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            metrics_artifact = {
                "accuracy_score": accuracy,
                "f1_score": f1,
                "precision": precision,
                "recall": recall,
            }
            return best_model_details, metrics_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def _initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:

            logging.info("Loading Transformed Train file...")
            trasnformed_train_file_path = (
                self.data_transformation_artifact.transformed_training_file_path
            )
            logging.info("Loading the transformed test file ")
            transformed_test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            train_array = load_numpy_array_data(file_path=trasnformed_train_file_path)
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)
            best_model_details, metrics_artifact = self.get_model_object_and__metrics(
                train_array, test_array
            )
            
            preprocessed__model_object = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            if best_model_details.best_score < self.model_trainer_config.base_accuracy:
                logging.info("No best model found with score more than base score")
                raise CustomException(
                    "No best model found with score more than base score"
                )
            trained_model_object = best_model_details.best_model

            model = PredictModel(
                trained_model_object=trained_model_object,
                preprocessed_object=preprocessed__model_object,
            )
            save_object(self.model_trainer_config.trained_model_file_path, model)

            model_trainer_Details = ModelTrainerArtifact(
                is_trained="TRUE",
                message="",
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                model_metrics=metrics_artifact,
            )

            logging.info(f"Model Trainer Artifact details are: {model_trainer_Details}")
            return model_trainer_Details
        except Exception as e:
            raise CustomException(e, sys)
