import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer la imagen
img = cv2.imread("Pacientes_imagenes/paciente6_1/Captura_22.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir rangos de colorqq
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

lower_Violet = np.array([85, 4, 0]) 
upper_Violet = np.array([138, 219, 122]) 
mask_violet = cv2.inRange(hsv_img, lower_Violet, upper_Violet)

lower_pink = np.array([0, 0, 20])
upper_pink = np.array([179, 142, 255])
mask_pink = cv2.inRange(hsv_img, lower_pink, upper_pink)

lower_rosa_claro = np.array([160, 20, 180])
upper_rosa_claro = np.array([180, 100, 255])
mask_pink2= cv2.inRange(hsv_img, lower_rosa_claro, upper_rosa_claro)

lower_white = np.array([0, 0, 200])
upper_white = np.array([179, 30, 255])
mask_white = cv2.inRange(hsv_img, lower_white, upper_white)

lower_color_lavanda = np.array([111, 34, 246])
upper_color_lavanda = np.array([124, 143, 253])
mask_lavanda = cv2.inRange(hsv_img, lower_color_lavanda, upper_color_lavanda)

lower_color_morado = np.array([111, 34, 246])
upper_color_morado = np.array([124, 143, 253])
mask_lavanda = cv2.inRange(hsv_img, lower_color_morado, upper_color_morado)

lower_lavanda_negro = np.array([120, 30, 40])
upper_lavanda_negro = np.array([135, 100, 120])

mask_lavanda_obscuro = cv2.inRange(hsv_img, lower_lavanda_negro, upper_lavanda_negro)

lower_black = np.array([120, 30, 40])
upper_black = np.array([135, 120, 60])
mask_negro = cv2.inRange(hsv_img, lower_black, upper_black)

lower_azul_violeta = np.array([125, 50, 70])
upper_azul_violeta = np.array([145, 180, 255])
mask_negro_violeta = cv2.inRange(hsv_img, lower_azul_violeta, upper_azul_violeta)

lower_lavanda_violeta = np.array([120, 60, 130])
upper_lavanda_violeta = np.array([135, 180, 255])
mask_negro_violeta = cv2.inRange(hsv_img, lower_lavanda_violeta, upper_lavanda_violeta)

lower_violeta2 = np.array([110, 60, 150])
upper_violeta2 = np.array([140, 255, 255])
mask_violeta2 = cv2.inRange(hsv_img, lower_violeta2, upper_violeta2)

lower_violeta3 = np.array([110, 100, 60])
upper_violeta3= np.array([140, 255, 180])
mask_violeta3 = cv2.inRange(hsv_img, lower_violeta3, upper_violeta3)

lower_uv = np.array([123, 112, 103])
upper_uv = np.array([130, 208, 247])
mask_violeta4 = cv2.inRange(hsv_img, lower_uv, upper_uv)

lower_red1 = np.array([0, 45, 50])
upper_red1 = np.array([15, 255, 255])

lower_red2 = np.array([160, 45, 50])
upper_red2 = np.array([179, 255, 255])

lower_yellow = np.array([20, 80, 80])
upper_yellow = np.array([35, 255, 255])

lower_pale = np.array([8,  25, 140])
upper_pale = np.array([22, 70, 255])
lower_beige_yellow = np.array([15, 20, 120])
upper_beige_yellow = np.array([40, 110, 255])

lower_yellow = np.array([18, 40, 130])
upper_yellow = np.array([38, 160, 255])

mask_yellow2=cv2.inRange(hsv_img,lower_yellow,upper_yellow)

lower_flesh = np.array([5, 15, 120])
upper_flesh = np.array([25, 90, 255])

mask_flesh=cv2.inRange(hsv_img,lower_flesh,upper_flesh)

lower_red1 = np.array([0, 50, 80])
upper_red1 = np.array([15, 255, 255])

lower_tone = np.array([15, 25, 135])
upper_tone = np.array([40, 120, 255])
mask_tone=cv2.inRange(hsv_img,lower_tone,upper_tone)

mask_red1=cv2.inRange(hsv_img,lower_red1,upper_red1)
lower_red2 = np.array([165, 50, 80])
upper_red2 = np.array([179, 255, 255])

lower_yellow_carne = np.array([15, 40, 120])
upper_yellow_carne = np.array([20, 120, 230])
mask_YC=cv2.inRange(hsv_img,lower_yellow_carne,upper_yellow_carne)
mask_beige_yellow=cv2.inRange(hsv_img,lower_beige_yellow,upper_beige_yellow)
mask_rosa_palido=cv2.inRange(hsv_img,lower_pale,upper_pale)
mask_yellow=cv2.inRange(hsv_img,lower_yellow,upper_yellow)

mask_red =cv2.inRange(hsv_img,lower_red1, upper_red1)
mask_red2=cv2.inRange(hsv_img,lower_red2,upper_red2)





# Morfología
kernel = np.ones((5, 5), np.uint8)
mask_cyan = cv2.dilate(mask_cyan, kernel, iterations=5)
mask_cyan = cv2.erode(mask_cyan, kernel, iterations=1)

mask_blue = cv2.dilate(mask_blue, kernel, iterations=5)
mask_blue = cv2.erode(mask_blue, kernel, iterations=2)

mask_blue_sky = cv2.dilate(mask_blue_sky, kernel, iterations=20)
mask_blue_sky = cv2.erode(mask_blue_sky, kernel, iterations=4)

mask_carnita2=cv2.dilate(mask_carnita2,kernel,iterations=15)


mask_white=cv2.erode(mask_white,kernel,iterations=20)
mask_lavanda=cv2.dilate(mask_lavanda,kernel,iterations=10)
mask_lavanda_obscuro=cv2.erode(mask_lavanda_obscuro,kernel,iterations=10)

mask_violeta2=cv2.erode(mask_violeta2,kernel,iterations=5)
mask_pink=cv2.erode(mask_pink,kernel,iterations=1)
mask_red2 = cv2.dilate(mask_red2, kernel,iterations=20)
mask_pink2=cv2.dilate(mask_pink2,kernel,iterations=10)
mask_rosa_palido=cv2.erode(mask_rosa_palido,kernel,iterations=10)


# Sumar máscaras
#mask_sum = mask_pink+mask_cyan #365nm
#mask_sum =  mask_blue + mask_violeta3#405
mask_sum=mask_pink+mask_red2+mask_pink2+mask_carnita2+mask_pink2
#mask_sum=mask_YC
mask_sum = np.clip(mask_sum, 0, 255).astype(np.uint8)

# Eliminar fragmentos pequeños
mask_clean = np.zeros_like(mask_sum)
contours, _ = cv2.findContours(mask_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area >10000:
        cv2.drawContours(mask_clean, [cnt], -1, 255, thickness=cv2.FILLED)

# Aplicar máscara limpia a la imagenq
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
    eraser_radius = 20  # Tamaño inicial de la goma

    def draw_eraser(event, x, y, flags, param):
        global drawing, ix, iy, mask_main_resized, eraser_radius
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
            cv2.circle(mask_main_resized, (x, y), eraser_radius, 0, -1)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            cv2.circle(mask_main_resized, (x, y), eraser_radius, 0, -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.circle(mask_main_resized, (x, y), eraser_radius, 0, -1)

    cv2.namedWindow("Usa la goma para borrar (Presiona 'q' para salir)")
    cv2.setMouseCallback("Usa la goma para borrar (Presiona 'q' para salir)", draw_eraser)

    print("🧽 Usa el mouse para borrar partes no deseadas.")
    print("Presiona '+' para aumentar el tamaño de la goma.")
    print("Presiona '-' para disminuir el tamaño de la goma.")
    print("Presiona 'q' cuando termines.")

    while True:
        temp_img_resized = cv2.bitwise_and(img_resized, img_resized, mask=mask_main_resized)
        cv2.imshow("Usa la goma para borrar (Presiona 'q' para salir)", temp_img_resized)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+') or key == ord('='):
            eraser_radius = min(100, eraser_radius + 5)
            print(f"Tamaño de goma: {eraser_radius}")
        elif key == ord('-') or key == ord('_'):
            eraser_radius = max(1, eraser_radius - 5)
            print(f"Tamaño de goma: {eraser_radius}")

    cv2.destroyAllWindows()

    # Escalar máscara modificada al tamaño original
    mask_main = cv2.resize(mask_main_resized, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Aplicar nueva máscara
    img_masked = cv2.bitwise_and(img, img, mask=mask_main)
    img_masked_rgb = cv2.cvtColor(img_masked, cv2.COLOR_BGR2RGB)

    # === GUARDAR imagen final limpia ===
    cv2.imwrite("R1.png", img_masked)  # <-- Esta línea guarda la imagen

    print("Imagen editada guardada como 'R1.png'")

    # Mostrar imagen final
    plt.figure(figsize=(10, 5))
    plt.imshow(img_masked_rgb)
    plt.axis("off")
    plt.show()

else:
    print("No se encontró ningún contorno principal.")
