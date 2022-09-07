import numpy as np

from ml_models.titanic.main import get_trained_data, make_predict_survived
from ml_models.titanic.schemas import Passenger


def test_get_trained_data():
    result = get_trained_data()
    assert isinstance(result.get("data"), list)
    assert result.get("errors") is None


def test_make_predict_survived(passengers_test_input_data):
    X_test = passengers_test_input_data[["Pclass", "Sex", "Age", "Fare"]]
    result = make_predict_survived(input_data=X_test)
    predictions = result.get("predictions")

    assert isinstance(predictions, list)
    assert isinstance(predictions[0], np.integer)
    assert result.get("errors") is None
    assert len(predictions) == len(passengers_test_input_data)
