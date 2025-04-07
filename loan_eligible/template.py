from pathlib import Path
import os

folder_name = 'src'
file_list = [

    f'{folder_name}/__init__.py',
    # Creating COmponents folder
    f'{folder_name}/exception.py',
    f'{folder_name}/logger.py',
    f'{folder_name}/components/__init__.py',
    f'{folder_name}/components/data_ingestion.py',
    f'{folder_name}/components/data_validation.py',
    f'{folder_name}/components/data_transformation',
    f'{folder_name}/components/model_trainer',
    # Creating Configuration for database
    f'{folder_name}/configuration/__init__.py',
    f'{folder_name}/configuration/mongodb_connection.py',
    #Data Access
    f'{folder_name}/data_access/__init__.py',
    f'{folder_name}/data_access/ProjectData',
    #Creating the Constants
    f'{folder_name}/constants/__init__.py',
    f'{folder_name}/entity/__init__.py',
    f'{folder_name}/entity/config_entity',
    f'{folder_name}/entity/artifact_entity',
    f'{folder_name}/pipeline/__init__.py',
    f'{folder_name}/pipeline/training_pipeline.py',
    f'{folder_name}/utils/utils.py',
    "requirements.txt",
    "Dockerfile",
    "demo.py",
    "setup.py",

    "config/model.yaml",
    "config/schema.yaml"
]


for file_path in file_list:
    dir_name = os.path.dirname(file_path)

    if dir_name!='' and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(' ')
    


