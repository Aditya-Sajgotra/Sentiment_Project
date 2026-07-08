"""Module for loading model and getting predictions from it"""
from transformers import pipeline

model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
model.save_pretrained("./model")
MODEL_VERSION = "1.0.0"


def predict(text: str) -> dict:
    return model(text)[0]
