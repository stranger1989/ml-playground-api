import pytest

from ml_models.processing import load_dataset


@pytest.fixture()
def passengers_test_input_data():
    return load_dataset(file_name="titanic_test.csv")
