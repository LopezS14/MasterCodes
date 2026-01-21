import cv2 
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen en formato BGR
bgr_image = cv2.imread("data/Violeta R1.jpg")

# Convertir a HSV
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
#convertir a rgb a hvs 

# Separar los canales HSV
H, S, V = cv2.split(hsv_image)

# Calcular histogramas en HSV
histH = cv2.calcHist([H], [0], None, [180], [0, 180])  # Hue (0-180 en OpenCV)
histS = cv2.calcHist([S], [0], None, [255], [0, 255])  # Saturación (0-255)
histV = cv2.calcHist([V], [0], None, [255], [0, 255])  # Valor (0-255)

# Función para calcular lower y upper usando percentiles
def calcular_limites(canal, percentil_bajo=9, percentil_alto=95):
    lower = np.percentile(canal, percentil_bajo)
    upper = np.percentile(canal, percentil_alto)
    return int(lower), int(upper)

# Obtener valores lower y upper
h_lower, h_upper = calcular_limites(H)
s_lower, s_upper = calcular_limites(S)
v_lower, v_upper = calcular_limites(V)

# Crear los límites en HSV
lower_bound = np.array([h_lower, s_lower, v_lower])
upper_bound = np.array([h_upper, s_upper, v_upper])

print(f"Lower HSV: {lower_bound}")
print(f"Upper HSV: {upper_bound}")

# Graficar los histogramas
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(histH, color='r')
plt.title("Histograma del canal H")

plt.subplot(1, 3, 2)
plt.plot(histS, color='g')
plt.title("Histograma del canal S")

plt.subplot(1, 3, 3)
plt.plot(histV, color='b')
plt.title("Histograma del canal V")

plt.show()
