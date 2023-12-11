from src.preprocessing import run as run_preprocessing
from src.integrated import run as run_integrated
from src.join_datasets import run as run_join_datasets
from src.train import run as run_train
from src.grapihs import plots


import shimoku_api_python as Shimoku
import mlflow
from dotenv import load_dotenv
import os
load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:8084")
access_token = os.getenv('SHIMOKU_TOKEN')
universe_id: str = os.getenv('UNIVERSE_ID')
workspace_id: str = os.getenv('WORKSPACE_ID')


shimoku = Shimoku.Client(
    access_token=access_token,
    universe_id=universe_id,
)

shimoku.set_workspace(workspace_id)


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

if __name__ == "__main__":
    file_name = run_preprocessing()
    #shimoku_upload_html(shimoku, file_name, "preprocessing", 0)
    file_name = run_integrated()
    #shimoku_upload_html(shimoku, file_name, "integrated", 1)
    file_name = run_join_datasets()
    #shimoku_upload_html(shimoku, file_name, "join_datasets", 2)
    run_train()
    plots(shimoku_client=shimoku)