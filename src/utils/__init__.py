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
