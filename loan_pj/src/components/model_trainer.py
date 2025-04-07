import pandas as pd
import sys
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact, ModelEvaluationArtifact
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
from src.utils.utils import load_numpy
import mlflow.sklearn


class ModelTraining:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def model_training(self) -> ModelEvaluationArtifact:
        try:
            logging.info('Evaluation Started')

            # Load transformed training and testing data
            train_arr = load_numpy(self.data_transformation_artifact.transformed_train_path)
            test_arr = load_numpy(self.data_transformation_artifact.transformed_test_path)
            logging.info(f'Train len: {train_arr.shape} Test len: {test_arr.shape}')

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            print("Shape of X_train:", X_train.shape)

            # Decision Tree Hyperparameters
            criterion = 'entropy'
            max_depth = 5
            splitter = 'best'

            logging.info('Training model Start')
            model = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, splitter=splitter)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            # Evaluation Metrics
            acc_score = accuracy_score(y_test, y_pred)
            clf_report = classification_report(y_test, y_pred)
            conf_matrix = confusion_matrix(y_test, y_pred)
            prec_score = precision_score(y_test, y_pred)
            rec_score = recall_score(y_test, y_pred)
            

            logging.info(f'Accuracy score: {acc_score}')
            # logging.info(f'Classification report: \n{clf_report}')
            # logging.info(f'Confusion matrix: \n{conf_matrix}')
            logging.info(f'Precision score: {prec_score}')
            logging.info(f'Recall score: {rec_score}')

           

            logging.info('Start with MLflow')
            mlflow.set_experiment('ML Model')

            logging.info('Dump the model using pickle')

            new_data = np.array([[5, 150, 22.5, 2,109, 1, 1]])  
            prediction = model.predict(new_data)
            print(f"Predicted class****************: {prediction[0]}")

            with open('tree_model.pkl', 'wb') as f:
                pickle.dump(model, f)

            with mlflow.start_run() as run:
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("criterion", criterion)
                mlflow.log_param("splitter", splitter)
                mlflow.log_metric('Accuracy', acc_score)
                mlflow.log_metric('Precision Score', prec_score)
                mlflow.log_metric('Recall Score', rec_score)               
                mlflow.sklearn.log_model(model, "model")

                mlflow_run_id = run.info.run_id
                logging.info('Model Training Completed')

            model_evaluation_artifact = ModelEvaluationArtifact(
                accuracy=acc_score,
                precision=prec_score,
                recall=rec_score,
                classification_report=clf_report,
                mlflow_run_id=mlflow_run_id
            )
            logging.info(f'Model evaluation artifact: {model_evaluation_artifact}')
            return model_evaluation_artifact

        except Exception as e:
            raise MyException(e, sys)
