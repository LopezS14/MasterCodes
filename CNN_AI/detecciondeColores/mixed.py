import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Cargar la imagen
img = cv2.imread("data/Azul R2.JPG")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rangos HSV para azul oscuro
bound_lower = np.array([100, 100, 50])
bound_upper = np.array([109, 255, 255])

# Rangos HSV para cian
bound_lower2 = np.array([85, 100, 100])
bound_upper2 = np.array([100, 255, 255])

# Máscaras
mask_blue = cv2.inRange(hsv_img, bound_lower, bound_upper)
mask_cian = cv2.inRange(hsv_img, bound_lower2, bound_upper2)

# Operaciones morfológicas
kernel = np.ones((7, 7), np.uint8)
mask_blue = cv2.erode(mask_blue, kernel, iterations=11)
mask_blue = cv2.dilate(mask_blue, kernel, iterations=20)

mask_cian = cv2.erode(mask_cian, kernel, iterations=5)
mask_cian = cv2.dilate(mask_cian, kernel, iterations=10)

# Segmentaciones individuales
seg_blue = cv2.bitwise_and(img, img, mask=mask_blue)
seg_cian = cv2.bitwise_and(img, img, mask=mask_cian)

# Combinar ambas segmentaciones
seg_combined = cv2.addWeighted(seg_blue, 1.0, seg_cian, 1.0, 0)

# Encontrar contornos para azul oscuro
contours_blue, _ = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(seg_combined, contours_blue, -1, (0, 0, 255), 3)  # contornos en rojo

# Contornos para cian
contours_cian, _ = cv2.findContours(mask_cian.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(seg_combined, contours_cian, -1, (0, 255, 0), 3)  # contornos en verde

# Redimensionar imagen para interfaz
(h, w) = img.shape[:2]
new_width = 400
aspect_ratio = h / w
new_height = int(new_width * aspect_ratio)
resized_img = cv2.resize(seg_combined, (new_width, new_height))

# Convertir para Tkinter
img_pil = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))
img_tk = ImageTk.PhotoImage(img_pil)

# Interfaz gráfica
root = tk.Tk()
root.title("Segmentación de Azul y Cian")
label = tk.Label(root, image=img_tk)
label.image = img_tk
label.pack()
root.mainloop()
