import json
import logging
from typing import Any
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from ml_models.titanic.main import get_trained_data, make_predict_survived
from ml_models.titanic import schemas

titanic_router = APIRouter()
logger = logging.getLogger(__name__)


@titanic_router.get(
    "/titanic/trained_data", response_model=schemas.TrainedData, status_code=200
)
async def titanic_trained_data():
    results = get_trained_data()
    return results


@titanic_router.post(
    "/titanic/predict/survived",
    response_model=schemas.PredictSurvivedResults,
    status_code=200,
)
async def titanic_predict_survived(input_data: schemas.PredictionInputs) -> Any:
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))
    logger.info({"message": f"Making prediction on inputs: {input_data.inputs}"})
    results = make_predict_survived(input_data=input_df)
    if results["errors"] is not None:
        logger.warning(
            {"message": f"Prediction validation error: {results.get('errors')}"}
        )
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))
    logger.info({"message": f"Prediction results: {results.get('predictions')}"})
    return results
