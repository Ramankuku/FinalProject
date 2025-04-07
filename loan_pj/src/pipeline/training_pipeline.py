import sys
from src.logger import logging
from src.exception import MyException
from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig, DataTransformationConfig
from src.entity.artifact_entity import DataArtifactConfig, DataValidationArtifact, DataTransformationArtifact, ModelEvaluationArtifact
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining
class TrainPipe:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
    

    def final_data_ingestion(self):
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info('Perfomed DataIngestion')
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)
    
    def final_data_validation(self, data_ingestion_artifact:DataArtifactConfig)->DataValidationArtifact:
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Performed DataValidation')
            return data_validation_artifact

        
        except Exception as e:
            raise MyException(e, sys)
    
    def final_data_transformation(self, data_ingestion_artifact:DataArtifactConfig, data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact, 
                                                     data_transformation_config = self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_transformation()
            logging.info('Performed DataTransformation')
            return data_transformation_artifact

        except Exception as e:
            raise MyException(e, sys)
        
    
    def initialise_model(self, data_transformation_artifact:DataTransformationArtifact)->ModelEvaluationArtifact:
        try:
            model_training = ModelTraining(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = model_training.model_training()
            logging.info('Performed ModelTraining')
            return model_evaluation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.final_data_ingestion()
            data_validation_artifact = self.final_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.final_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            model_evaluation_artifact = self.initialise_model(data_transformation_artifact=data_transformation_artifact)
            logging.info(f'Model evaluation artifact: {model_evaluation_artifact}')

            
        except Exception as e:
            raise MyException(e, sys)