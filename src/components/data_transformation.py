from matplotlib.pyplot import step
from numpy import save
from traitlets import import_item
from src.entity.estimator import TargetValueMapping
from src.logger import logging
from src.constant import CURRENT_YEAR, SCHEMA_FILE_PATH, TARGET_COLUMN
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
)
from src.entity.config_entity import DataTransformationConfig
from src.exception import CustomException
from src.utils import (
    drop_columns,
    read_from_csv_file,
    read_yaml_file,
    save_numpy_array_data,
    save_object,
    sys,
    pd,
    np,
)
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    OrdinalEncoder,
    PowerTransformer,
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from imblearn.combine import SMOTEENN

# from imblearn.over_sampling import SMOTE


class DataTransformation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_configuration = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformation_object(self) -> Pipeline:
        try:

            logging.info("Inside the get data transformation object class...")

            standard_scaler_transformer = StandardScaler()
            one_hot_transformer = OneHotEncoder()
            ordnal_encoder_transformer = OrdinalEncoder()
            power_transformer = PowerTransformer()
            logging.info("Created objects for different transformers...")

            num_features = self.schema_configuration["num_features"]
            or_columns = self.schema_configuration["or_columns"]
            oh_columns = self.schema_configuration["oh_columns"]
            transform_columns = self.schema_configuration["transform_columns"]

            logging.info("creating power transformers...")
            transform_pipeline = Pipeline(
                steps=[
                    (
                        "power_transformer",
                        PowerTransformer(method="yeo-johnson"),
                    )
                ]
            )
            preprocessor = ColumnTransformer(
                [
                    ("onehot_encoder", one_hot_transformer, oh_columns),
                    ("ordinal_columns", ordnal_encoder_transformer, or_columns),
                    ("Transformer", transform_pipeline, transform_columns),
                    ("Standard Scaler", standard_scaler_transformer, num_features),
                ]
            )
            logging.info(
                "Initialized column transformer with necessary transformations..."
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_target_column(
        self, df: pd.DataFrame, target, is_training_df: bool = True
    ):

        try:
            df["company_age"] = CURRENT_YEAR - df["yr_of_estab"]
            msg = "created new column 'company age in"
            msg2 = " training data" if is_training_df else "testing data"

            logging.info(f"Created new column 'company_age' in the {msg+msg2}...")
            cols_to_drop = self.schema_configuration["drop_columns"]
            df = drop_columns(df=df, cols=cols_to_drop)
            target = target.apply(lambda x: 1 if x == "Certified" else 0)
            return df, target
        except Exception as e:
            raise CustomException(e, sys)

    def get_input_and_output_features(self, target_feature, df: pd.DataFrame):
        input_features = df.drop(columns=target_feature, axis=1)
        target_feature = df[target_feature]

        return input_features, target_feature

    def initiate_data_transformations(self) -> DataTransformationArtifact:
        try:
            if not self.data_validation_artifact.validation_status:
                raise CustomException(self.data_validation_artifact.message, sys)
            logging.info("Inside the data transformation component...")
            preprocessor = self.get_data_transformation_object()
            training_dataframe = read_from_csv_file(
                file_path=self.data_ingestion_artifact.train_file_path
            )
            testing_dataframe = read_from_csv_file(
                file_path=self.data_ingestion_artifact.test_file_path
            )
            train_input_dataframe, train_target_dataframe = (
                self.get_input_and_output_features(
                    target_feature=TARGET_COLUMN, df=training_dataframe
                )
            )
            test_input_dataframe, test_target_dataframe = (
                self.get_input_and_output_features(
                    target_feature=TARGET_COLUMN, df=testing_dataframe
                )
            )

            logging.info(
                f"Columns in the training features are: {train_input_dataframe.columns}"
            )
            logging.info(f"Target feature: {train_target_dataframe.name}")
            train_input_features, train_target_dataframe = (
                self.preprocess_target_column(
                    df=train_input_dataframe, target=train_target_dataframe
                )
            )
            test_input_features, test_target_dataframe = self.preprocess_target_column(
                df=test_input_dataframe,
                is_training_df=False,
                target=test_target_dataframe,
            )
            train_input_features_numpy_arr = preprocessor.fit_transform(
                train_input_features
            )
            test_input_features_numpy_arr = preprocessor.transform(test_input_features)
            logging.info(
                "transformed the train/test input features with preprocessor object..."
            )
            logging.info(
                "Applying SMOTEEN on the training data to handle imbalance issues"
            )
            smt = SMOTEENN(sampling_strategy="minority")

            final_train_input_features, final_train_target_feature = smt.fit_resample(
                train_input_features_numpy_arr, train_target_dataframe
            )
            logging.info("Applied  SMOTEEN on the training dataset")
            logging.info("Applying SMOTEEN on the testing dataset")
            final_test_input_features, final_test_target_features = smt.fit_resample(
                test_input_features_numpy_arr, test_target_dataframe
            )
            logging.info("Applied SMOTEEN on the testing dataset")

            train_data = np.c_[
                final_train_input_features, np.array(final_train_target_feature)
            ]

            test_data = np.c_[
                final_test_input_features, np.array(final_test_target_features)
            ]

            save_object(
                file_path=self.data_transformation_config.preprocessed_object_file_path,
                obj=preprocessor,
            )
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_data,
            )
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_data,
            )

            data_transformation_artifact_details = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.preprocessed_object_file_path,
                transformed_training_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            logging.info(
                f"Data transformation artifact details are: {data_transformation_artifact_details}"
            )
            return data_transformation_artifact_details
        except Exception as e:
            raise CustomException(e, sys)
