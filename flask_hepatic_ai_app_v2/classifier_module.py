# classifier_module.py
import os
from PIL import Image
import numpy as np

import tf_keras
from tf_keras.models import load_model
from tf_keras.preprocessing.image import img_to_array
from tf_keras.applications.mobilenet_v2 import preprocess_input

IMG_WIDTH, IMG_HEIGHT = 224, 224
CLASES = ["2w", "8w", "12w", "Control"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "mix_model_weavelenght.h5")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Carga legacy (H5) con Keras 2 API
modelo = load_model(MODEL_PATH, compile=False)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def procesar_y_predecir(ruta_imagen: str):
    img = Image.open(ruta_imagen).convert("RGB")
    img_resized = img.resize((IMG_WIDTH, IMG_HEIGHT))

    img_array = img_to_array(img_resized)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    pred = modelo.predict(img_array)
    pred_clase = CLASES[int(np.argmax(pred))]

    resultado = f"Prediction: Week {pred_clase}\n\nmodel certainty:\n"
    for clase, prob in zip(CLASES, pred[0]):
        resultado += f"{clase}: {prob:.2f}\n"

    return pred_clase, resultado