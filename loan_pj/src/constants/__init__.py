import os
from datetime import date

#Constants used for DATABASE
DB_NAME = 'LoanPredictionData'
CONNECTION_NAME = 'LoanPredictionData-Data'
MONGODB_URL_KEY = 'MONGODB_URL'
SCHEMA_FILE_PATH = os.path.join('config', 'schema.yaml')
PIPELINE_NAME: str = ''
ARTIFACT_DIR: str = 'artifact'
FILE_NAME:str = 'data.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
PREPROCESSED_FILE: str = 'processing.pkl' 


#Constants for DATA_INGESTION
DATA_INGESTION_COLLECTION_NAME:str = 'LoanPredictionData-Data'

DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


DATA_VALIDATION_DIR_NAME = 'validated'
DATA_VALIDATION_SCHEMA_FILE = 'report.yaml'
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformed'
DATA_TRANSFORMATION_TRANSFORMED_FILE: str = 'transformed'
DATA_TRANSFORMED_OBJECT_TRANSFORMED_FILE: str= 'object-transformed'

TARGET='Personal Loan'