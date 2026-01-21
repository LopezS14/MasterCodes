import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Cargar la imagen
img = cv2.imread("detecciondeColores/test/captura_0.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir los rangos de color
# Azul
bound_lower_blue = np.array([100, 100, 50])
bound_upper_blue = np.array([109, 255, 255])

# Blanco
bound_lower_white = np.array([0, 0, 200])
bound_upper_white = np.array([180, 30, 255])

# Violeta
bound_lower_violet = np.array([125, 50, 50])
bound_upper_violet = np.array([150, 255, 255])

# Aplicar las máscaras
mask_blue = cv2.inRange(hsv_img, bound_lower_blue, bound_upper_blue)
mask_white = cv2.inRange(hsv_img, bound_lower_white, bound_upper_white)
mask_violet = cv2.inRange(hsv_img, bound_lower_violet, bound_upper_violet)

# Combinar las máscaras
mask_combined = cv2.bitwise_or(mask_blue, mask_white)
mask_combined = cv2.bitwise_or(mask_combined, mask_violet)

# Operaciones morfológicas para eliminar ruido
kernel = np.ones((7, 7), np.uint8)
mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)
mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel)

# Aplicar la máscara a la imagen original
seg_img = cv2.bitwise_and(img, img, mask=mask_combined)

# Encontrar y dibujar contornos
contours, _ = cv2.findContours(mask_combined.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(seg_img, contours, -1, (0, 0, 255), 3)

# Redimensionar la imagen para la interfaz
(h, w) = img.shape[:2]
new_width = 500
aspect_ratio = h / w
new_height = int(new_width * aspect_ratio)
resized_img = cv2.resize(seg_img, (new_width, new_height))

# Convertir a formato PIL para Tkinter
img_pil = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Segmentación de colores (Azul, Blanco, Violeta)")

# Guardar la imagen en una variable global para evitar que se elimine
img_tk = ImageTk.PhotoImage(img_pil)

# Mostrar la imagen en un Label
label = tk.Label(root, image=img_tk)
label.image = img_tk  # Se almacena en el atributo del Label para evitar eliminación por GC
label.pack()

# Ejecutar la ventana
root.mainloop()