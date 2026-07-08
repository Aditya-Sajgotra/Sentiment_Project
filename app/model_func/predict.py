"""Module for loading model and getting predictions from it"""
from transformers import pipeline
MODEL_VERSION = "1.0.0"

def get_model():

    model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return model

def predict(input: str) -> dict:
    model = get_model()
    return model.predict(input)
