from typing import Any, List, Optional
import numpy as np
import pandas as pd
import logging
from pydantic import BaseModel, Extra, ValidationError

logger = logging.getLogger(__name__)


class Passenger(BaseModel, extra=Extra.forbid):
    Pclass: int
    Sex: str
    Age: int
    Fare: float


class PredictionInputs(BaseModel):
    inputs: List[Passenger]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "Pclass": 1,
                        "Sex": "male",
                        "Age": 20,
                        "Fare": 160.5,
                    }
                ]
            }
        }


class PredictSurvivedResults(BaseModel):
    predictions: List[int]
    errors: Optional[Any]


class TrainedData(BaseModel):
    data: List[Passenger]
    errors: Optional[Any]


def validate_input_data(*, input_data: pd.DataFrame) -> Optional[str]:
    errors = None
    try:
        PredictionInputs(
            inputs=input_data.replace({np.nan: 0}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()
        logger.error({"model validation error occurred": f": {errors}"})
    return errors
