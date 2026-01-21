import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen
img = cv2.imread("detecciondeColores/test/captura_0.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir rangos de color
lower_cyan = np.array([80, 80, 100])
upper_cyan = np.array([100, 255, 255])
mask_cyan = cv2.inRange(hsv_img, lower_cyan, upper_cyan)

lower_blue = np.array([85, 50, 50])
upper_blue = np.array([109, 255, 255])
mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)

lower_skyblue = np.array([90, 50, 100])
upper_skyblue = np.array([120, 255, 255])
mask_blue_sky = cv2.inRange(hsv_img, lower_skyblue, upper_skyblue)

lower_carnita = np.array([0, 0, 0])     
upper_carnita = np.array([179, 203, 255])  
mask_carnita = cv2.inRange(hsv_img, lower_carnita, upper_carnita)

lower_carnita_clara = np.array([0, 15, 120])
upper_carnita_clara = np.array([20, 90, 255])
mask_carnita2 = cv2.inRange(hsv_img, lower_carnita_clara, upper_carnita_clara)


lower_Violet=np.array([85, 4, 0]) 
upper_Violet=np.array([138, 219, 122]) 
mask_violet = cv2.inRange(hsv_img, lower_Violet, upper_Violet)

lower_pink =np.array ([0, 0, 20])
upper_pink =np.array ([179, 142, 255])
mask_pink= cv2.inRange(hsv_img, lower_pink, upper_pink)

lower_rosa_claro = np.array([160, 20, 180])
upper_rosa_claro = np.array([180, 100, 255])
mask_pink2= cv2.inRange(hsv_img, lower_rosa_claro, upper_rosa_claro)


lower_white = np.array([0, 0, 200])
upper_white = np.array([179, 30, 255])
mask_white = cv2.inRange(hsv_img, lower_white, upper_white)


# Morfología
kernel = np.ones((5, 5), np.uint8)
mask_cyan = cv2.dilate(mask_cyan, kernel, iterations=5)
mask_cyan = cv2.erode(mask_cyan, kernel, iterations=1)

mask_blue = cv2.dilate(mask_blue, kernel, iterations=5)
mask_blue = cv2.erode(mask_blue, kernel, iterations=2)

mask_blue_sky = cv2.dilate(mask_blue_sky, kernel, iterations=5)
mask_blue_sky = cv2.erode(mask_blue_sky, kernel, iterations=5)

mask_carnita2=cv2.dilate(mask_carnita2,kernel,iterations=5)

# Sumar máscaras
mask_sum =  mask_violet
mask_sum = np.clip(mask_sum, 0, 255).astype(np.uint8)

# Eliminar fragmentos pequeños
mask_clean = np.zeros_like(mask_sum)
contours, _ = cv2.findContours(mask_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
#<350000 para detectar objetos pequeños
    if area <1000:
        cv2.drawContours(mask_clean, [cnt], -1, 255, thickness=cv2.FILLED)

# Aplicar máscara limpia a la imagen
segmented_img = cv2.bitwise_and(img, img, mask=mask_clean)
segmented_rgb = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB)

# Buscar contorno principal
contours_clean, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours_clean:
    main_contour = max(contours_clean, key=cv2.contourArea)
    area_objeto = cv2.contourArea(main_contour)
    print(f"Área del objeto de interés: {area_objeto:.2f} píxeles²")

    # Crear máscara del contorno principal
    mask_main = np.zeros_like(mask_clean)
    cv2.drawContours(mask_main, [main_contour], -1, 255, thickness=cv2.FILLED)

    # === GOMA para borrar partes no deseadas ===
    fixed_width = 500
    scale = fixed_width / img.shape[1]
    resized_size = (fixed_width, int(img.shape[0] * scale))

    img_resized = cv2.resize(img, resized_size, interpolation=cv2.INTER_AREA)
    mask_main_resized = cv2.resize(mask_main, resized_size, interpolation=cv2.INTER_NEAREST)

    drawing = False
    ix, iy = -1, -1

    def draw_eraser(event, x, y, flags, param):
        global drawing, ix, iy, mask_main_resized
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            cv2.circle(mask_main_resized, (x, y), 20, 0, -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.circle(mask_main_resized, (x, y), 20, 0, -1)

    cv2.namedWindow("Usa la goma para borrar (Presiona 'q' para salir)")
    cv2.setMouseCallback("Usa la goma para borrar (Presiona 'q' para salir)", draw_eraser)

    print("🧽 Usa el mouse para borrar partes no deseadas. Pulsa 'q' cuando termines.")
    while True:
        temp_img_resized = cv2.bitwise_and(img_resized, img_resized, mask=mask_main_resized)
        cv2.imshow("Usa la goma para borrar (Presiona 'q' para salir)", temp_img_resized)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

    # Escalar máscara modificada al tamaño original
    mask_main = cv2.resize(mask_main_resized, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Aplicar nueva máscara
    img_masked = cv2.bitwise_and(img, img, mask=mask_main)
    img_masked_rgb = cv2.cvtColor(img_masked, cv2.COLOR_BGR2RGB)

    # === GUARDAR imagen final limpia ===
    cv2.imwrite("R1.png", img_masked)  # <-- Esta línea guarda la imagen

    print("Imagen editada guardada como 'RC1q.png'")

    # Mostrar imagen final
    plt.figure(figsize=(10, 5))
    plt.imshow(img_masked_rgb)
    #plt.title("Imagen limpia con fondo negro")
    plt.axis("off")
    plt.show()

else:
    print("No se encontró ningún contorno principal.")
