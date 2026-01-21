import cv2
import os
from gtts import gTTS
import pygame
import tempfile
import threading
import time

# ----------- Cargar modelo entrenado ----------
method = 'LBPH'
if method == 'LBPH':
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
elif method == 'Eigen':
    emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
elif method == 'Fisher':
    emotion_recognizer = cv2.face.FisherFaceRecognizer_create()

emotion_recognizer.read('modelo' + method + '.xml')
# ----------------------------------------------

dataPath = 'dataEmotion'
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Función para hablar las recomendaciones
def speak(text):
    temp_audio_file = None
    try:
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='es')
        tts.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name
        temp_audio_file.close()

        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if temp_audio_file:
            try:
                os.unlink(temp_audio_file_path)
            except PermissionError:
                pass

# Recomendaciones por emoción
def get_emotion_recommendation(emotion_label):
    recommendations = {
        'Felicidad': 'Me alegro mucho de que estés feliz, sigue disfrutando tu día.',
        'Tristeza': 'Busca siempre el equilibrio entre tus responsabilidades y tu bienestar personal.',
        'Enojo': 'Respira hondo y relájate, es importante mantener la calma. La ira puede provocar que hagas cosas de las que luego te arrepientas.',
        'Miedo': 'Tómate un momento para analizar lo inesperado antes de actuar.',
    }
    return recommendations.get(emotion_label, "No puedo procesar tu emoción en este momento.")

# Variable para evitar repetir la misma emoción hablada
last_spoken_emotion = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        try:
            result = emotion_recognizer.predict(rostro)
            label = result[0]

            if label < len(imagePaths):
                emotion = imagePaths[label]

                cv2.putText(frame, '{}'.format(emotion), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if emotion != last_spoken_emotion:
                    last_spoken_emotion = emotion
                    recommendation = get_emotion_recommendation(emotion)
                    threading.Thread(target=speak, args=(recommendation,)).start()
        except Exception as e:
            print("Error al predecir emoción:", e)

    cv2.imshow('Ejecutando Análisis', frame)
    k = cv2.waitKey(1)
    if k == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
1