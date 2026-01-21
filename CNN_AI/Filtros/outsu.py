import cv2
import numpy as np
import matplotlib.pyplot as plt

# --- Paso 1: Leer y convertir la imagen ---
img = cv2.imread("data/2 semanas/455nm/Copy of Azul RC1.JPG")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# --- Paso 2: Crear máscaras por rangos de color ---

# Cian
lower_cyan = np.array([80, 80, 100])
upper_cyan = np.array([100, 255, 255])
mask_cyan = cv2.inRange(hsv_img, lower_cyan, upper_cyan)
kernel = np.ones((5, 5), np.uint8)
mask_cyan = cv2.dilate(mask_cyan, kernel, iterations=5)
mask_cyan = cv2.erode(mask_cyan, kernel, iterations=6)

# Azul
lower_blue = np.array([85, 50, 50])
upper_blue = np.array([109, 255, 255])
mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
mask_blue = cv2.dilate(mask_blue, kernel, iterations=13)
mask_blue = cv2.erode(mask_blue, kernel, iterations=19)

# Azul cielo
lower_skyblue = np.array([90, 50, 100])
upper_skyblue = np.array([120, 255, 255])
mask_blue_sky = cv2.inRange(hsv_img, lower_skyblue, upper_skyblue)
mask_blue_sky = cv2.dilate(mask_blue_sky, kernel, iterations=5)
mask_blue_sky = cv2.erode(mask_blue_sky, kernel, iterations=47)

# --- Paso 3: Combinar las máscaras y aplicar a la imagen original ---
mask_sum = mask_cyan + mask_blue + mask_blue_sky
mask_sum = np.clip(mask_sum, 0, 255)
segmented_img = cv2.bitwise_and(img, img, mask=mask_sum)

# --- Paso 4: Crear máscara binaria para análisis de contornos ---
segmented_gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)
_, refined_mask = cv2.threshold(segmented_gray, 1, 255, cv2.THRESH_BINARY)

# --- Paso 5: Encontrar y filtrar contornos pequeños ---
contours, _ = cv2.findContours(refined_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_area = 20000  # Área mínima para mantener (ajustable)
new_mask = np.zeros_like(refined_mask)

for contour in contours:
    if cv2.contourArea(contour) > min_area:
        cv2.drawContours(new_mask, [contour], -1, 255, thickness=cv2.FILLED)

# --- Paso 6: Aplicar la máscara limpia a la imagen original ---
final_result = cv2.bitwise_and(img, img, mask=new_mask)
final_rgb = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)

# --- Paso 7: Mostrar y guardar resultado ---
plt.figure(figsize=(10, 5))
plt.imshow(final_rgb)
plt.title("Objeto principal sin el anillo")
plt.axis("off")
plt.show()

cv2.imwrite("mascara_filtrada.png", new_mask)
print("✅ Máscara guardada como 'mascara_filtrada.png'")
