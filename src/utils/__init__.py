import os
import sys
from dotenv import load_dotenv
import yaml
import json
import dill
from src.exception import CustomException
from src.logger import logging
from datetime import datetime
import pandas as pd
import numpy as np

timestamp_format = "%Y-%m-%d_%H-%M-%S"


def load_environmental_variables():
    load_dotenv()


def get_environment_variables(variable_name: str) -> str:
    load_environmental_variables()
    return os.getenv(variable_name)


def read_yaml_file(filename):
    try:

        with open(file=filename) as file:
            logging.info(f"Reading YAML File from {filename} location...")
            data = yaml.safe_load(file)
            logging.info(f"Successfully read YAML File present in {filename} location")
            return data

    except Exception as e:
        raise CustomException(e)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys) from e


def get_current_timestamp():
    return datetime.now().strftime(timestamp_format)


def read_from_csv_file(file_path: str) -> pd.DataFrame:
    try:
        logging.info(f"reading csv file at: {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Finished reading csv file at: {file_path}")
        return df
    except Exception as e:
        raise CustomException(e)


def load_object(file_path: str) -> object:
    logging.info("Loading the model object....")

    try:
        with open(file_path, "rb") as file:
            obj = dill.load(file)
            logging.info("Successfully Loaded model object ......")
            return obj

    except Exception as e:
        raise CustomException(e)


def save_object(file_path: str, obj: object) -> None:
    logging.info("Inside the save_object method")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info(f"successfully saved the object at {file_path}")

    except Exception as e:
        raise CustomException(e, sys) from e


def drop_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    logging.info("Started dropping columns from the dataframe")

    try:
        df = df.drop(columns=cols, axis=1)

        logging.info(f"Successfully dropped {cols} from the dataframe")

        return df
    except Exception as e:
        raise CustomException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):

    try:
        logging.info("Inside the save numpy_array_data function")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
        logging.info(f"Saved the numpy array at {file_path}")
    except Exception as e:
        raise CustomException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:

    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj, allow_pickle=True)
    except Exception as e:
        raise CustomException(e, sys) from e
