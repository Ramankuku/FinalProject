import os
import sys
from pandas import DataFrame
from src.constants import *
from src.logger import logging
from src.exception import MyException
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataArtifactConfig
from src.data_access.ProjectData import Proj1Data


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise MyException(e,sys)
    




    def export_feature_store(self)->DataFrame:
        logging.info('Start fecting data from Database')
        try:
            loan_data = Proj1Data()
            dataframe = loan_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f'Data fetched from Database: {dataframe.shape}')
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            dir_name= os.path.dirname(feature_store_path)
            os.makedirs(dir_name, exist_ok=True)
            logging.info('Saving the exporting data in Feature Store')
            dataframe.to_csv(feature_store_path,index=False,header=True)
            logging.info('Data saved in Feature Store')
            return dataframe    
        except Exception as e:
            raise MyException(e,sys)
    

    def split_data(self, dataframe:DataFrame)->None:
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Splitting done')
            logging.info(f'Train set : {train_set.shape} and Test set : {test_set}')
 
            dir_path = self.data_ingestion_config.training_file_path
            dir_names=os.path.dirname(dir_path)
            os.makedirs(dir_names, exist_ok=True)

            train_set = train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set = test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info('Saving train and test split')
        except Exception as e:
            raise MyException(e,sys)
    

    def initiate_data_ingestion(self)->DataArtifactConfig:
        logging.info('Calling all the functions')
        try:
            dataframe = self.export_feature_store()
            logging.info('Exporting data')
            self.split_data(dataframe)
            logging.info('Splitting the data')

            data_artifact_config = DataArtifactConfig(train_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)

            return data_artifact_config          
        
        except Exception as e:
            raise MyException(e,sys)
