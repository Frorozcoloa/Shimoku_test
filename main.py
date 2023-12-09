from src.preprocessing import run as run_preprocessing
from src.integrated import run as run_integrated
from src.join_datasets import run as run_join_datasets
from src.train import run as run_train

if __name__ == "__main__":
    run_preprocessing()
    run_integrated()
    run_join_datasets()
    run_train()