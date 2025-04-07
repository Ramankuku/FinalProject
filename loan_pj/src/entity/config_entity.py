import os
import sys
from dataclasses import dataclass
from src.constants import *
from datetime import datetime


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class DataPipeLineConfig:
    pipeline_name:str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str=TIMESTAMP

data_pipeline_config = DataPipeLineConfig = DataPipeLineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(data_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name: str = DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_validation_dir = os.path.join(data_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    validation_file_path = os.path.join(data_validation_dir, DATA_VALIDATION_SCHEMA_FILE)


    
    
@dataclass
class DataTransformationConfig:
    data_transformation_dir = os.path.join(data_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_FILE, TRAIN_FILE_NAME.replace('csv', 'npy'))
    transformed_test_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_FILE, TEST_FILE_NAME.replace('csv', 'npy'))
    transformed_object_path = os.path.join(data_transformation_dir, DATA_TRANSFORMED_OBJECT_TRANSFORMED_FILE, PREPROCESSED_FILE)
    

