"""Module for loading model and getting predictions from it"""
from transformers import pipeline

model = pipeline("sentiment-analysis", model="./model")
model.save_pretrained("./model")
MODEL_VERSION = "1.0.0"


def predict(input: str) -> dict:
    return model.predict(input)
