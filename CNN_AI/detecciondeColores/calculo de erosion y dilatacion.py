import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Leer imagen
img = cv2.imread("data/Azul R2.JPG")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rangos de colores
# Azul oscuro
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([109, 255, 255])
# Cian
lower_cian = np.array([85, 100, 100])
upper_cian = np.array([100, 255, 255])

# Función para actualizar la imagen
def actualizar():
    erosion_val = erosion_scale.get()
    dilation_val = dilatacion_scale.get()
    erosion_val_cian = erosion_scale2.get()
    dilation_val_cian = dilatacion_scale2.get()
    shape = kernel_var.get()

    # Tipo de kernel
    if shape == "Rect":
        shape_type = cv2.MORPH_RECT
    elif shape == "Elliptic":
        shape_type = cv2.MORPH_ELLIPSE
    else:
        shape_type = cv2.MORPH_CROSS

    kernel = cv2.getStructuringElement(shape_type, (7, 7))

    # Máscaras originales
    mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    mask_cian = cv2.inRange(hsv_img, lower_cian, upper_cian)

    # Procesamiento morfológico para azul
    mask_blue = cv2.erode(mask_blue, kernel, iterations=erosion_val)
    mask_blue = cv2.dilate(mask_blue, kernel, iterations=dilation_val)

    # Procesamiento morfológico para cian
    mask_cian = cv2.erode(mask_cian, kernel, iterations=erosion_val_cian)
    mask_cian = cv2.dilate(mask_cian, kernel, iterations=dilation_val_cian)

    # Aplicar ambas máscaras
    seg_blue = cv2.bitwise_and(img, img, mask=mask_blue)
    seg_cian = cv2.bitwise_and(img, img, mask=mask_cian)

    # Combinar segmentaciones
    seg_combined = cv2.addWeighted(seg_blue, 1.0, seg_cian, 1.0, 0)

    # Dibujar contornos
    contours_blue, _ = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_cian, _ = cv2.findContours(mask_cian.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(seg_combined, contours_blue, -1, (0, 0, 255), 2)  # Azul en rojo
    cv2.drawContours(seg_combined, contours_cian, -1, (0, 255, 0), 2)  # Cian en verde

    # Redimensionar para la interfaz
    img_resized = cv2.resize(seg_combined, (400, 300))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Mostrar en panel
    panel.config(image=img_tk)
    panel.image = img_tk

# Crear ventana principal
ventana = Tk()
ventana.title("Segmentación Azul y Cian con Erosión/Dilatación")

# Menú para seleccionar forma del kernel
kernel_var = StringVar(value="Rect")
OptionMenu(ventana, kernel_var, "Rect", "Elliptic", "Cross", command=lambda _: actualizar()).pack()

# Sliders para azul
erosion_scale = Scale(ventana, from_=0, to=400, orient=HORIZONTAL, label="Erosión Azul", command=lambda _: actualizar())
erosion_scale.pack()

dilatacion_scale = Scale(ventana, from_=0, to=400, orient=HORIZONTAL, label="Dilatación Azul", command=lambda _: actualizar())
dilatacion_scale.pack()

# Sliders para cian
erosion_scale2 = Scale(ventana, from_=0, to=400, orient=HORIZONTAL, label="Erosión Cian", command=lambda _: actualizar())
erosion_scale2.pack()

dilatacion_scale2 = Scale(ventana, from_=0, to=400, orient=HORIZONTAL, label="Dilatación Cian", command=lambda _: actualizar())
dilatacion_scale2.pack()

# Panel para mostrar la imagen
panel = Label(ventana)
panel.pack()

# Mostrar imagen inicial
actualizar()

ventana.mainloop()
