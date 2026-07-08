"""Module for loading model and getting predictions from it"""
from transformers import pipeline

model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
MODEL_VERSION = "1.0.0"


def predict(input: str) -> dict:
    return model.predict(input)
