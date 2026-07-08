import pytest
import unittest.mock as mock
import json
import db.main
import model_func 
from app.app import Input, get_response,check_health
from db.main import input_data,Data,metadata,Base,engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import ValidationError


@pytest.mark.parametrize(
    "user_input, Sentiment,Confidence",
    [("Im good", "POSITIVE", "99"), ("Im sad", "NEGATIVE", "99")],
)
@mock.patch("app.app.input_data")
@mock.patch("app.app.predict")
def test_get_response(mock_predict, mock_input_data, user_input, Sentiment, Confidence):
    mock_predict.return_value = [{"label": Sentiment, "score": Confidence}]

    data = Input(input=user_input)
    response = get_response(data)

    assert json.loads(response.body) == {
        "sentiment": Sentiment,
        "confidence": Confidence,
    }
    
def test_check_health():
    model_func.predict.MODEL_VERSION = "1.0.0"
    model_func.predict.model = 1 
    response = check_health()
    assert json.loads(response.body) == {"model version": "1.0.0", "is model loaded": True}
    
def test_input_data():
    test_engine = create_engine("sqlite:///:memory:")
    db.main.engine = test_engine
    
    Base.metadata.create_all(test_engine)
    
    input_data(input="Im sad",sentiment_output = "POSITIVE",confidence=0.99)
    
    with Session(test_engine) as session:
       result = session.query(Data).all()
       assert len(result) == 1
       assert result[0].input == "Im sad"
       assert result[0].sentiment_output == "POSITIVE"
       assert result[0].confidence == 0.99
       
def test_get_response_error():
    with pytest.raises(ValidationError):
        user_input = Input(input = 123)
        get_response(user_input)
    