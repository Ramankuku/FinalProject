from dataclasses import dataclass

@dataclass
class DataArtifactConfig:
    train_file_path: str
    test_file_path: str
    

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    validation_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_path: str
    transformed_train_path: str
    transformed_test_path: str
    

@dataclass
class ModelEvaluationArtifact:
    accuracy: float  
    precision: float 
    recall: float
    classification_report: str
    mlflow_run_id: str