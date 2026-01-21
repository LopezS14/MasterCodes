import cv2
import os
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

def obtenerModelo(method, facesData, labels):
    if method == 'EigenFaces': 
        emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
    elif method == 'FisherFaces': 
        emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
    elif method == 'LBPH': 
        emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

    print("Entrenando ( {} )...".format(method))
    inicio = time.time()
    emotion_recognizer.train(facesData, np.array(labels))
    tiempoEntrenamiento = time.time() - inicio
    print("Tiempo de entrenamiento ( {} ): ".format(method), tiempoEntrenamiento)

    emotion_recognizer.write("modelo{}.xml".format(method))
    return emotion_recognizer

# Ruta a tus datos
dataPath = 'dataEmotion'
emotionsList = os.listdir(dataPath)
print('Lista de emociones: ', emotionsList)

labels = []
facesData = []

label = 0

# Cargar imágenes
for nameDir in emotionsList:
    emotionsPath = os.path.join(dataPath, nameDir)
    for fileName in os.listdir(emotionsPath):
        image = cv2.imread(os.path.join(emotionsPath, fileName), 0)
        if image is not None:
            image = cv2.resize(image, (150, 150), interpolation=cv2.INTER_CUBIC)
            facesData.append(image)
            labels.append(label)
    label += 1

# Convertir a numpy
facesData = np.array(facesData)
labels = np.array(labels)

# Dividir en entrenamiento y prueba (stratify para que se conserve proporción de clases)
X_train, X_test, y_train, y_test = train_test_split(
    facesData, 
    labels, 
    test_size=0.2, 
    stratify=labels, 
    random_state=42
)

# Entrenar el modelo
modelo = obtenerModelo('LBPH', X_train, y_train)

# Evaluar el modelo
y_pred = []
total_eval = len(X_test)

print("\n🔍 Realizando predicciones para generar matriz de confusión...\n")
for i, img in enumerate(X_test):
    label_pred, _ = modelo.predict(img)
    y_pred.append(label_pred)
    porcentaje = (i + 1) / total_eval * 100
    print(f"\r⏳ Predicción {i + 1}/{total_eval} ({porcentaje:.1f}%)", end='', flush=True)

# Matriz de confusión
print("\n\n✅ Predicciones completadas. Generando matriz de confusión...\n")
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=emotionsList)
print("📋 Reporte de clasificación:\n")
print(report)

# Visualización de la matriz
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', xticklabels=emotionsList, yticklabels=emotionsList)
plt.title('Matriz de Confusión')
plt.xlabel('Predicción')
plt.ylabel('Etiqueta Verdadera')
plt.tight_layout()
plt.show()
