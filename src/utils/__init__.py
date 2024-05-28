import os
import sys
import yaml
import json
from src.exception import CustomException
from src.logger import logging
from datetime import datetime
import pandas as pd

timestamp_format = "%Y-%m-%d_%H-%M-%S"


def read_yaml_file(filename):
    try:

        with open(file=filename) as file:
            logging.info(f"Reading YAML File from {filename} location...")
            data = yaml.safe_load(file)
            logging.info(f"Successfully read YAML File present in {filename} location")
            return data

    except Exception as e:
        raise CustomException(e)


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
