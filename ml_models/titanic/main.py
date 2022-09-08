from typing import Union
import numpy as np
import pandas as pd

from ml_models.processing import load_dataset, load_pipeline
from ml_models.titanic.schemas import validate_input_data


def get_trained_data() -> dict:
    df = load_dataset(file_name="titanic/train.csv")
    X = df[["Pclass", "Sex", "Age", "Fare"]]
    results = {"data": X.replace({np.nan: 0}).to_dict(orient="records"), "errors": None}
    return results


def make_predict_survived(
    *,
    input_data: Union[pd.DataFrame, dict],
) -> dict:
    errors = validate_input_data(input_data=input_data)
    trained_model = load_pipeline(file_name="titanic_predict_model.pkl")
    results = {"predictions": list(trained_model.predict(input_data)), "errors": errors}
    return results
