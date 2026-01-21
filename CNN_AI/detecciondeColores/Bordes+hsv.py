import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen
img = cv2.imread("detecciondeColores/test/captura_0.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir rangos de color (puedes ajustarlos según tu caso)
lower_cyan = np.array([80, 80, 100])
upper_cyan = np.array([100, 255, 255])
mask_cyan = cv2.inRange(hsv_img, lower_cyan, upper_cyan)

lower_carnita = np.array([0, 0, 0])     
upper_carnita = np.array([179, 203, 255])  
mask_carnita = cv2.inRange(hsv_img, lower_carnita, upper_carnita)

#lower_carnita = [0, 0, 0]

#upper_carnita = [179, 203, 255]

lower_blue = np.array([0,20,70])
upper_blue = np.array([25, 150, 255])
mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)

lower_skyblue = np.array([90,50,100])
upper_skyblue = np.array([120,255,255])
mask_blue_sky = cv2.inRange(hsv_img, lower_skyblue, upper_skyblue)

# Morfología para limpiar las máscaras
kernel = np.ones((5,5), np.uint8)
mask_cyan = cv2.dilate(mask_cyan, kernel, iterations=10)
mask_cyan = cv2.erode(mask_cyan, kernel, iterations=1)

mask_blue = cv2.dilate(mask_blue, kernel, iterations=5)
mask_blue = cv2.erode(mask_blue, kernel, iterations=4)

mask_blue_sky = cv2.dilate(mask_blue_sky, kernel, iterations=5)
mask_blue_sky = cv2.erode(mask_blue_sky, kernel, iterations=5)

# Sumar las máscaras
mask_sum = mask_carnita
mask_sum = np.clip(mask_sum, 0, 255).astype(np.uint8)

# Eliminar el fragmento no deseado usando contornos
mask_clean = np.zeros_like(mask_sum)
contours, _ = cv2.findContours(mask_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area >1000:  # umbral para eliminar fragmentos pequeños
        cv2.drawContours(mask_clean, [cnt], -1, 255, thickness=cv2.FILLED)


# Aplicar la máscara limpia a la imagen original
segmented_img = cv2.bitwise_and(img, img, mask=mask_clean)
segmented_rgb = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB)

# === Identificar el contorno principal (más grande RETR_EXTERNAL) CHAIN_APRROX_SIMPLE (Guarda los puntos del contorno) 
contours_clean, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours_clean:
    # Contorno más grande
    main_contour = max(contours_clean, key=cv2.contourArea)

    # Calcular el área
    area_objeto = cv2.contourArea(main_contour)
    print(f"Área del objeto de interés: {area_objeto:.2f} píxeles²")

    # Crear una máscara negra para el contorno principal
    mask_main = np.zeros_like(mask_clean)
    cv2.drawContours(mask_main, [main_contour], -1, 255, thickness=cv2.FILLED)

    # Aplicar la máscara a la imagen original para que el fondo quede negro fuera del contorno principal
    img_masked = cv2.bitwise_and(img, img, mask=mask_main)
    img_masked_rgb = cv2.cvtColor(img_masked, cv2.COLOR_BGR2RGB)

    # Mostrar la imagen con el contorno dibujado
    contoured_img = segmented_rgb.copy()
    cv2.drawContours(contoured_img, [main_contour], -1, (255, 0, 0), 2)

    plt.figure(figsize=(10,5))
    plt.imshow(contoured_img)
    plt.title("Contorno del objeto de interés")
    plt.axis("off")
    plt.show()

    # Mostrar la imagen con fondo negro fuera del contorno principal
    plt.figure(figsize=(10,5))
    #plt.imshow(img_masked_rgb)
    #plt.savefig("RC2.png", bbox_inches='tight', pad_inches=0, facecolor='black')  # Guardar imagen
    #plt.title("Imágen limpia")
    plt.axis("off")
    #plt.show()



else:
    print("No se encontró ningún contorno principal.")
