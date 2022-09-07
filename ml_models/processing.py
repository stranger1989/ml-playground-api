from pathlib import Path
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator

from ml_models.config import ROOT_PATH


def load_dataset(*, file_name: str) -> pd.DataFrame:
    df = pd.read_csv(Path(f"{ROOT_PATH}/datasets/{file_name}"))
    return df


def save_pipeline(*, pipeline: Pipeline, file_name: str) -> None:
    joblib.dump(pipeline, f"{ROOT_PATH}/trained_models/{file_name}")


def load_pipeline(*, file_name: str) -> BaseEstimator:
    return joblib.load(filename=f"{ROOT_PATH}/trained_models/{file_name}")
