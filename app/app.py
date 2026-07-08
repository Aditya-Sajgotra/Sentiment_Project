"""Sentimenat Analysis with fastapi postgres and data validation"""

from typing import Annotated, Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from db.main import input_data
from model_func.predict import predict,MODEL_VERSION,get_model


app = FastAPI()


class Input(BaseModel):
    """Basic structure of how an input should look like"""
    id: Annotated[
        Optional[int],
        Field(description="Id for identification of the input", examples=[1, 2]),
    ] = None
    input: Annotated[
        str, Field(..., description="Input text to be analysed", max_length=100)
    ]


@app.post("/predict")
def get_response(data: Input) -> JSONResponse:
    """It returns a response corresponding to user's input"""
    output = predict(data.input)
    output_label = output[0]['label']
    output_score = output[0]["score"]
    input_data(input = data.input,sentiment_output = output_label,confidence=output_score)
    return JSONResponse(
        status_code=200,
        content={"sentiment": output_label, "confidence": output_score},
    )


@app.get("/health")
def check_health() -> JSONResponse:
    """Mehtod for checking health of the model or website"""
    model = get_model()
    return JSONResponse(
        status_code=200,
        content={"model version": MODEL_VERSION, "is model loaded": model is not None},
    )
