from src.logger import logging
from src.exception import CustomException
from src.utils import sys


class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1

    def _asdict(self):
        return self.__dict__


class PredictModel:

    def __init__(self, trained_model_object, preprocessed_object) -> None:
        self.trained_model_object = trained_model_object
        self.preprocessed_object = preprocessed_object

    def predict(self, dataframe):
        logging.info("Inside the Model prediction function:....")
        try:
            logging.info("Transforming the dataframe with pre-traned model object...")
            transformed_feature = self.preprocessed_object.transform(dataframe)
            logging.info("predicting the features with pre-trained model object...")
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise CustomException(e, sys)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
