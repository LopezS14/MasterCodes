import random
import subprocess
import threading
import json
import pickle
import numpy as np
import streamlit as st
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from streamlit_mic_recorder import speech_to_text  # <-- NUEVO


# --- Carga de recursos ---
lemmatizer = WordNetLemmatizer()
nltk.download("punkt", quiet=True)  # evita fallo en tokenización

@st.cache_resource
def load_assets():
    intents = json.loads(open("intents.json", encoding="utf-8").read())
    words = pickle.load(open("words.pkl", "rb"))
    classes = pickle.load(open("classes.pkl", "rb"))
    model = load_model("chatbot_model.h5")
    return intents, words, classes, model

intents, words, classes, model = load_assets()

# --- Utilidades NLP ---
def clean_up_sentence(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return [lemmatizer.lemmatize(w) for w in tokens]

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag, dtype=np.float32)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    idx = int(np.argmax(res))
    return classes[idx]

def get_response(tag, intents_json):
    for it in intents_json["intents"]:
        if it["tag"] == tag:
            return random.choice(it["responses"])
    return "No entendí, ¿puedes decirlo de otra forma?"

# --- Lanzar análisis sin bloquear ---
def run_analysis_async():
    try:
        # Usa Popen para no bloquear el hilo principal de Streamlit
        subprocess.Popen(["python", "emotionRecognition.py"])
        st.session_state["analysis_status"] = "Ejecutando análisis…"
    except Exception as e:
        st.session_state["analysis_status"] = f"Error al iniciar análisis: {e}"

# --- Estado de la conversación ---
if "chat" not in st.session_state:
    st.session_state.chat = []
if "analysis_status" not in st.session_state:
    st.session_state.analysis_status = "Listo"

# --- UI: dos columnas ---
col_chat, col_vis = st.columns([1, 1])

with col_chat:
    st.title("Hope_Beta 001")
    st.write("Te doy la bienvenida, estoy aquí para ayudarte.")

    # Mostrar historial
    for speaker, msg in st.session_state.chat:
        st.markdown(f"**{speaker}:** {msg}")

    user_msg = st.text_input("Estoy para ti, ¿qué necesitas?", key="user_input")
    c1, c2 = st.columns(2)
    with c1:
        send = st.button("💬 Enviar")
    with c2:
        analyze = st.button("▶️Analízame")

    if send and user_msg.strip():
        st.session_state.chat.append(("Tú", user_msg))
        try:
            tag = predict_class(user_msg)
            bot_msg = get_response(tag, intents)
            st.session_state.chat.append(("Bot", bot_msg))

            # Si el intent es "analisis", dispara la cámara/visión
            if tag == "analisis":
                threading.Thread(target=run_analysis_async, daemon=True).start()
        except Exception as e:
            st.error(f"Ocurrió un error procesando tu mensaje: {e}")

    if analyze:
        threading.Thread(target=run_analysis_async, daemon=True).start()
        st.session_state.chat.append(("Bot", "Iniciando análisis…"))


    # Muestra una imagen/placeholder si tienes un frame reciente guardado:
    # st.image("frame_actual.jpg", caption="Detección de emoción", use_container_width=True)

# --- Depuración visible (evita pantalla negra silenciosa) ---
#st.sidebar.info("Si la pantalla queda en negro, revisa el log/errores aquí.")
