import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Cargar la imagen
img = cv.imread('data/Azul R2.jpg')
assert img is not None, "No se pudo cargar la imagen"

# Convertir a HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Definir el rango de color del objeto 
#Definiendo el rando del interior del hígado
lower_color = np.array([100,100,50]) #Canales h,s,v Min
upper_color = np.array([109, 255, 255])#Canales h,s, v Max
lower_color2=np.array([])#canales hsv

# Crear máscara en base al color
mask_color = cv.inRange(hsv, lower_color, upper_color)

# Aplicar morfología para mejorar la máscara
kernel = np.ones((5,5), np.uint8)
mask_color = cv.morphologyEx(mask_color, cv.MORPH_CLOSE, kernel)

# Crear la máscara para GrabCut
mask = np.zeros(img.shape[:2], np.uint8)
mask[mask_color > 0] = cv.GC_FGD  # Los píxeles detectados como color deseado son primer plano
mask[mask_color == 0] = cv.GC_BGD  # Los otros son fondo

# Modelos de fondo y primer plano (requeridos por GrabCut)

import cv2 as cv
from matplotlib import pyplot as plt

# Cargar la imagen
img = cv.imread('data/Azul R2.jpg')
assert img is not None, "No se pudo cargar la imagen"

# Convertir a HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Definir el rango de color del objeto (ajustar según la imagen)
lower_color = np.array([100,100,50]) #Canales h,s,v Min
upper_color = np.array([109, 255, 255])#Canales h,s, v Max

# Crear máscara en base al color
mask_color = cv.inRange(hsv, lower_color, upper_color)

# Aplicar morfología para mejorar la máscara
kernel = np.ones((5,5), np.uint8)
mask_color = cv.morphologyEx(mask_color, cv.MORPH_CLOSE, kernel)

# Crear la máscara para GrabCut
mask = np.zeros(img.shape[:2], np.uint8)
mask[mask_color > 0] = cv.GC_FGD  # Los píxeles detectados como color deseado son primer plano
mask[mask_color == 0] = cv.GC_BGD  # Los otros son fondo

# Modelos de fondo y primer plano (requeridos por GrabCut)
bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

# Aplicar GrabCut con la máscara inicial
cv.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK)

# Crear una máscara binaria donde 1 es objeto y 0 es fondo
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Aplicar la máscara a la imagen original para quitar el fondo
img_resultado = img * mask2[:, :, np.newaxis]

# Mostrar resultado
plt.imshow(cv.cvtColor(img_resultado, cv.COLOR_BGR2RGB))
plt.title('Segmentación con HSV + GrabCut')
plt.show()
np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

# Aplicar GrabCut con la máscara inicial
cv.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK)

# Crear una máscara binaria donde 1 es objeto y 0 es fondo
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Aplicar la máscara a la imagen original para quitar el fondo
img_resultado = img * mask2[:, :, np.newaxis]

# Mostrar resultado
plt.imshow(cv.cvtColor(img_resultado, cv.COLOR_BGR2RGB))
plt.title('Segmentación con HSV + GrabCut')
plt.show()
