import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen
img = cv2.imread("data/Azul R2.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir rangos de color para cian, azul, azul cielo
lower_cyan = np.array([80, 80, 100])
upper_cyan = np.array([100, 255, 255])
mask_cyan = cv2.inRange(hsv_img, lower_cyan, upper_cyan)

lower_blue = np.array([60, 60, 100])
upper_blue = np.array([109, 255, 255])
mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)

lower_skyblue = np.array([90, 50, 100])
upper_skyblue = np.array([120, 255, 255])
mask_blue_sky = cv2.inRange(hsv_img, lower_skyblue, upper_skyblue)

# Crear una máscara para el fondo (en este caso azul, según el rango que has dado)
lower_background = np.array([100, 100, 100])
upper_background = np.array([140, 255, 255])
mask_background = cv2.inRange(hsv_img, lower_background, upper_background)

# Dilatar y erode las máscaras para limpiar y mejorar la segmentación
kernel = np.ones((5,5), np.uint8)

# Erosión y dilatación en las máscaras
mask_cyan = cv2.dilate(mask_cyan, kernel, iterations=2)
mask_blue = cv2.dilate(mask_blue, kernel, iterations=2)
mask_blue_sky = cv2.dilate(mask_blue_sky, kernel, iterations=2)

# Sumar las máscaras de cian, azul y azul cielo
mask_sum = mask_blue + mask_cyan + mask_blue_sky
mask_sum = np.clip(mask_sum, 0, 255)  # Asegurar que no se pase de 255

# Aplicar la máscara combinada de colores
segmented_img = cv2.bitwise_and(img, img, mask=mask_sum)

# Hacer el fondo negro utilizando la máscara de fondo
background_black = cv2.bitwise_and(img, img, mask=mask_background)
background_black[:] = 0  # Establecer los píxeles del fondo a negro

# Combinar la imagen segmentada con el fondo negro
final_result = cv2.bitwise_or(segmented_img, background_black)

# Convertir BGR a RGB para visualizar con matplotlib
final_rgb = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)

# Mostrar el resultado final
plt.figure(figsize=(10, 5))
plt.imshow(final_rgb)
plt.title("Segmentación con fondo negro")
plt.axis("off")
plt.show()
