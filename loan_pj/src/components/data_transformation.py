import pandas as pd
import sys
import numpy as np
from src.constants import SCHEMA_FILE_PATH, TARGET
from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from src.entity.artifact_entity import DataArtifactConfig, DataValidationArtifact, DataTransformationArtifact
from src.exception import MyException
from src.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer
from src.utils.utils import read_yaml_file, save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataArtifactConfig, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self.schema_file = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)

    def preprocess_data_transformation(self) -> Pipeline:
        try:
            ordinal_features = self.schema_file['ordinal_feature']
            categorical_features= self.schema_file['categorical_feature']
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('ordinal', OrdinalEncoder(), ordinal_features),
                    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_features)
                ],



                remainder='passthrough' 
            )

            pipeline = Pipeline(steps=[('Preprocessor', preprocessor)])
            return pipeline
        except Exception as e:
            raise MyException(e, sys)

    def drop_columns(self, df):
        logging.info(f'========= {df.shape}')
        drop_cols = self.schema_file['drop_columns']
        df = df.drop(columns=[col for col in drop_cols if col in df.columns], axis=1)
        logging.info(f'========= {df.shape}')
        return df
    
    def convert_ccavg(self, df):
        logging.info('Converting ccavg to float')
        convert_cols = self.schema_file['ccavg']
        for col in convert_cols:  
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('/', '.')
                df[col] = df[col].astype(float) * 12
                logging.info(f'********* {df.shape}')
        
        return df

    def initiate_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = self.read_data(file_path=self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info(f'######## {train_df.shape}')
            train_df[TARGET] = train_df[TARGET].map({'Yes': 1, 'No': 0})
            test_df[TARGET] = test_df[TARGET].map({'Yes': 1, 'No': 0})
            logging.info('Mapping of Target column Done')

            input_features_train_df = train_df.drop(columns=[TARGET], axis=1)
            target_feature_train_df = train_df[TARGET].values.reshape(-1, 1) 
            logging.info(f'######## Dropping Target Value from train_df: {input_features_train_df.shape}')
            
            input_features_test_df = test_df.drop(columns=[TARGET], axis=1)
            target_feature_test_df = test_df[TARGET].values.reshape(-1, 1)  

            input_features_train_df = self.drop_columns(input_features_train_df)
            input_features_test_df = self.drop_columns(input_features_test_df)

            input_features_train_df = self.convert_ccavg(input_features_train_df)
            input_features_test_df = self.convert_ccavg(input_features_test_df)
            
            # processor = self.preprocess_data_transformation()
            # processor.fit(input_features_train_df)  
            # feature_names = processor.get_feature_names_out()
            # print("Transformed Features:", feature_names)


            processor = self.preprocess_data_transformation()
            

            input_features_train_arr = processor.fit_transform(input_features_train_df)
            input_features_test_arr = processor.transform(input_features_test_df)
            logging.info(f'Input Feature: {input_features_train_arr.shape} ----- {input_features_test_arr.shape}-------')

            # Ensure target variable has the same number of rows
            train_arr = np.c_[input_features_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_features_test_arr, np.array(target_feature_test_df)]

            logging.info(f'TRAIN ARR---------- {train_arr.shape}')

            save_object(self.data_transformation_config.transformed_object_path, processor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_path, array=test_arr)

            return DataTransformationArtifact(
                transformed_object_path=self.data_transformation_config.transformed_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path
            )

        except Exception as e:
            raise MyException(e, sys)