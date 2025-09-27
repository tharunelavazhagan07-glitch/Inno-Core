import io
import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os
from dotenv import load_dotenv
from .utils import map_severity, combine_predictions

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "./weights.h5")
ADVICE_PATH = os.path.join(os.path.dirname(__file__), "advice.json")

def load_model_and_classes():
    model = load_model(MODEL_PATH)
    with open(ADVICE_PATH, "r", encoding="utf-8") as f:
        advice_json = json.load(f)
    classes = list(advice_json.keys())
    return model, classes, advice_json

async def predict_disease(files, types, language="en"):
    model, classes, advice_json = load_model_and_classes()
    predictions_list = []
    for file in files:
        img = Image.open(io.BytesIO(await file.read())).convert("RGB")
        img = img.resize((224,224))
        img_arr = img_to_array(img)/255.0
        img_arr = np.expand_dims(img_arr, axis=0)
        preds = model.predict(img_arr)[0]
        predictions_list.append(preds)
    final_probs = combine_predictions(predictions_list)
    results = []
    for i, cls in enumerate(classes):
        advice_text = advice_json[cls].get(language, advice_json[cls]["en"])
        results.append({
            "class": cls,
            "probability": float(final_probs[i]),
            "severity": map_severity(final_probs[i]),
            "advice": advice_text
        })
    return results
