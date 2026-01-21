import cv2
import os
import requests
import numpy as np
import re

emotionName = 'Felicidad'
dataPath = 'dataEmotion'
emotionsPath = os.path.join(dataPath, emotionName)

if not os.path.exists(emotionsPath):
    print('Carpeta creada!', emotionsPath)
    os.makedirs(emotionsPath)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

image_urls = [
   


]   

max_samples = 50

# Función para obtener el siguiente índice a usar
def obtener_ultimo_indice(path):
    archivos = os.listdir(path)
    indices = []
    for archivo in archivos:
        match = re.match(r'rostro_(\d+)\.jpg', archivo)
        if match:
            indices.append(int(match.group(1)))
    if len(indices) == 0:
        return 0
    else:
        return max(indices) + 1

indice_actual = obtener_ultimo_indice(emotionsPath)

for url in image_urls:
    # Descargar imagen
    response = requests.get(url)
    arr = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        print(f'Error cargando {url}')
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print('No se encontraron caras')
        continue

    x, y, w, h = faces[0]
    rostro_original = image[y:y+h, x:x+w]

    count = 0
    while count < max_samples:
        rostro = rostro_original.copy()

        dx = np.random.randint(-10, 11)
        dy = np.random.randint(-10, 11)

        x1 = max(0, x + dx)
        y1 = max(0, y + dy)
        x2 = min(image.shape[1], x1 + w)
        y2 = min(image.shape[0], y1 + h)

        rostro_var = image[y1:y2, x1:x2]
        rostro_var = cv2.resize(rostro_var, (150, 150), interpolation=cv2.INTER_CUBIC)

        alpha = 1.0 + np.random.uniform(-0.3, 0.3)
        beta = np.random.randint(-20, 20)
        rostro_var = cv2.convertScaleAbs(rostro_var, alpha=alpha, beta=beta)

        angle = np.random.uniform(-15, 15)
        M = cv2.getRotationMatrix2D((75, 75), angle, 1)
        rostro_var = cv2.warpAffine(rostro_var, M, (150, 150))

        nombre = os.path.join(emotionsPath, f'rostro_{indice_actual}.jpg')
        cv2.imwrite(nombre, rostro_var)
        print(f'Guardado: {nombre}')

        indice_actual += 1
        count += 1

print(f'Total {indice_actual} imágenes guardadas en {emotionsPath}')
