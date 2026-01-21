import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar imagen
img = cv2.imread('data/Azul R2.JPG')  # Reemplaza con la ruta de tu imagen
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir a RGB para matplotlib

# Aplicar Filtro Pasa Bajas
blur = cv2.blur(img, (15, 15))  # Filtro de media
gaussian = cv2.GaussianBlur(img, (15, 15), 0)  # Filtro Gaussiano

# Convertir a RGB para visualización
blur_rgb = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
gaussian_rgb = cv2.cvtColor(gaussian, cv2.COLOR_BGR2RGB)

# Mostrar imágenes
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
axs[0].imshow(img_rgb)
axs[0].set_title('Imagen Original')
axs[0].axis('off')

axs[1].imshow(blur_rgb)
axs[1].set_title('Filtro de Media')
axs[1].axis('off')

axs[2].imshow(gaussian_rgb)
axs[2].set_title('Filtro Gaussiano')
axs[2].axis('off')

plt.show()
