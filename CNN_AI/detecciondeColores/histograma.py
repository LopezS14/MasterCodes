import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen
img_path = cv.imread('data/Azul R2.jpg')

# Canales de la imagen
R = img_path[:, :, 0]
G = img_path[:, :, 1]
B = img_path[:, :, 2]

# Conversión de RGB a escala de grises
A = (0.299 * R)
A2 = (0.587 * G)
A3 = (0.114 * B)
AT = (A + A2 + A3)

# Conversión a enteros
entero = AT.astype(np.uint8)

# Umbralización
m, n = np.shape(entero)
for i in range(m):
    for j in range(n):
        if entero[i, j] >100:
            entero[i, j] = 0
        else:
            entero[i, j] = 1
MatrizTrans=np.transpose(entero)
#Matriz transpuesta de la transpuesta
Girar=np.transpose(MatrizTrans)
# Calcular el histograma
hist = cv.calcHist([entero], [0], None, [255], [0, 255])

# Mostrar histograma
plt.subplot(1,4,1)
plt.imshow(hist)
plt.title("Histograma de la imagen binarizada")
plt.xlabel("Valor de píxel")
plt.ylabel("Frecuencia")
plt.subplot(1,4,2)
plt.imshow(entero,cmap='gray')
plt.subplot(1,4,3)
plt.imshow(MatrizTrans)
plt.subplot(1,4,4)
plt.imshow(Girar)

#plt.figure(2)
#plt.plot(m,n)
plt.show()
