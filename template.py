from pathlib import Path
import os

project_name = "us_visa_approval"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/s3_operation.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/pipeline/train_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/ml/__init__.py",
    f"{project_name}/ml/feature",
    f"{project_name}/ml/models",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml"

]


for filepath in list_of_files:
    filepath = Path(filepath)
    file_directory, file_name = os.path.split(filepath)
    if file_directory !="":
        os.makedirs(file_directory, exist_ok=True)
    if (not os.path.exists(filepath) ) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print("File already exists at: {filepath}")