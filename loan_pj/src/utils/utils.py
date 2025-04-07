import os
import sys
import dill
import yaml
import numpy as np
from pandas import DataFrame
from src.exception import MyException
from src.logger import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV


def read_yaml_file(file_path: str)->dict:
    try:
        with open (file_path, 'rb') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    except Exception as e:
        raise MyException(e, sys)
    

def load_object(file_path: str)->object:
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise MyException(e, sys)


def load_numpy(file_path: str) -> np.ndarray:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)  # Fix: allow_pickle=True
    except Exception as e:
        raise MyException(e, sys)


def save_object(file_path: str, obj:object)->None:
    logging.info("Entering into save_object function")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            logging.info("Object saved successfully")
            
    except Exception as e:
        raise MyException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
   
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MyException(e, sys) from e
    

