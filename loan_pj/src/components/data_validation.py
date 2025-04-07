import os
import sys
import json
import pandas as pd
from pandas import DataFrame
from src.constants import SCHEMA_FILE_PATH
from src.exception import MyException
from src.logger import logging
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataArtifactConfig, DataValidationArtifact
from src.utils.utils import read_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataArtifactConfig, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_file = read_yaml_file(file_path=SCHEMA_FILE_PATH)

    def is_validate(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self.schema_file['columns'])
            logging.info(f'Status is: [{status}]')
            return status
        except Exception as e:
            raise MyException(e, sys) from e

    def is_column_exist(self, df:DataFrame)->bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns= []
            missing_categorical_columns = []

            
            for column in self.schema_file['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            
            if len(missing_numerical_columns) > 0:
                logging.info(f'Missing numerical columns: {missing_numerical_columns}')
            

            for column in self.schema_file['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            
            if len(missing_categorical_columns) > 0:
                logging.info(f'Missing numerical columns: {missing_categorical_columns}')
            
            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns) > 0 else True
        
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_mess = ''
            logging.info("Data validation started")

            train_df, test_df = (
                DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            )

            logging.info('Train and test dataframes are read')

            # Validate train data
            status = self.is_validate(dataframe=train_df)
            if not status:
                validation_mess += 'Some columns are missing in train data. '
            else:
                logging.info(f'Train data columns validation status: {status}')

            # Validate test data
            status = self.is_validate(dataframe=test_df)
            if not status:
                validation_mess += 'Some columns are missing in test data. '
            else:
                logging.info(f'Test data columns validation status: {status}')

            validation_status = len(validation_mess) == 0  # True if no issues

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_mess.strip(),
                validation_report_file_path=self.data_validation_config.validation_file_path
            )

            dir_path = os.path.dirname(self.data_validation_config.validation_file_path)
            os.makedirs(dir_path, exist_ok=True)

            validation_report = {
                'validation_status': validation_status,
                'message': validation_mess.strip()
            }

            with open(self.data_validation_config.validation_file_path, 'w') as file:
                json.dump(validation_report, file, indent=4)

            logging.info(f'Saved validation report: {validation_report}')

            return data_validation_artifact 

        except Exception as e:
            raise MyException(e, sys)
