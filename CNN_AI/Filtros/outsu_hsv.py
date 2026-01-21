import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Cargar la imagen
img = cv2.imread("data/Azul R2.JPG")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir los rangos de color azul en HSV
bound_lower = np.array([100, 100, 50])  # Canales H, S, V Min
bound_upper = np.array([109, 255, 255])  # Canales H, S, V Max

# Aplicar la máscara
mask_blue = cv2.inRange(hsv_img, bound_lower, bound_upper)

# Operaciones morfológicas para eliminar ruido
kernel = np.ones((7, 7), np.uint8)
mask_blue = cv2.erode(mask_blue, kernel, iterations=11)
mask_blue = cv2.dilate(mask_blue, kernel, iterations=20)

# Aplicar la máscara a la imagen original
seg_img = cv2.bitwise_and(img, img, mask=mask_blue)

# Convertir la imagen a escala de grises para aplicar Otsu
gray_img = cv2.cvtColor(seg_img, cv2.COLOR_BGR2GRAY)

# Aplicar el umbral de Otsu
_, otsu_mask = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Combinar la segmentación de color con Otsu
combined_mask = cv2.bitwise_and(mask_blue, otsu_mask)
seg_combined = cv2.bitwise_and(img, img, mask=combined_mask)

# Encontrar y dibujar contornos
contours, _ = cv2.findContours(combined_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(seg_combined, contours, -1, (0, 0, 255), 3)

# Redimensionar la imagen para la interfaz
(h, w) = img.shape[:2]
new_width = 400
aspect_ratio = h / w
new_height = int(new_width * aspect_ratio)
resized_img = cv2.resize(seg_combined, (new_width, new_height))

# Convertir a formato PIL para Tkinter
img_pil = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Segmentación de color azul con Otsu")

# Guardar la imagen en una variable global para evitar que se elimine
img_tk = ImageTk.PhotoImage(img_pil)

# Mostrar la imagen en un Label
label = tk.Label(root, image=img_tk)
label.image = img_tk  # Se almacena en el atributo del Label para evitar eliminación por GC
label.pack()

# Ejecutar la ventana
root.mainloop()
