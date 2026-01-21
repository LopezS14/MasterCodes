import cv2
import numpy as np

# Variables globales para la selección del ROI
start_x, start_y, end_x, end_y = -1, -1, -1, -1
drawing = False

# Función para dibujar el rectángulo (ROI) con el ratón
def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_x, end_y = x, y
            temp_img = resized_img.copy()  # Copia temporal de la imagen redimensionada
            cv2.rectangle(temp_img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow("Selecciona la región", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y
        cv2.rectangle(resized_img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imshow("Selecciona la región", resized_img)

# Cargar la imagen (supón que el usuario sube la imagen en formato binario)
img = cv2.imread('data/Azul R2.jpg', 0)

# Verificar si la imagen se carga correctamente
if img is None:
    print("Error al cargar la imagen. Verifica la ruta.")
    exit()

# Redimensionar la imagen para ajustar el tamaño a la ventana
height, width = img.shape
resize_factor = 0.5  # Ajusta este valor según el tamaño que prefieras
resized_img = cv2.resize(img, (int(width * resize_factor), int(height * resize_factor)))

# Mostrar la imagen redimensionada para que el usuario seleccione la región
cv2.imshow("Selecciona la región", resized_img)
cv2.setMouseCallback("Selecciona la región", draw_rectangle)

# Esperar a que el usuario seleccione la región
cv2.waitKey(0)
cv2.destroyAllWindows()

# Verificar que el usuario haya seleccionado la región correctamente
if start_x != -1 and start_y != -1 and end_x != -1 and end_y != -1:
    if end_x > start_x and end_y > start_y:
        # Ajustar las coordenadas del ROI para la imagen original
        start_x_org = int(start_x / resize_factor)
        start_y_org = int(start_y / resize_factor)
        end_x_org = int(end_x / resize_factor)
        end_y_org = int(end_y / resize_factor)

        # Definir el ROI seleccionado en la imagen original
        roi = img[start_y_org:end_y_org, start_x_org:end_x_org]

        # Crear un kernel para las operaciones morfológicas
        kernel = np.ones((5, 5), np.uint8)  # Ajusta el tamaño según lo necesites

        # Aplicar erosión o dilatación al ROI
        erosion = cv2.erode(roi, kernel, iterations=1)
        dilatacion = cv2.dilate(roi, kernel, iterations=1)

        # Crear una imagen de salida con el resto de la imagen eliminada
        result_img = np.zeros_like(img)  # Crear una imagen vacía de la misma forma
        result_img[start_y_org:end_y_org, start_x_org:end_x_org] = erosion  # O usa 'dilatacion' si prefieres dilatación

        # Mostrar la imagen resultante
        cv2.imshow("Imagen con erosión aplicada", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Guardar la imagen resultante si lo deseas
        cv2.imwrite('resultado.jpg', result_img)
    else:
        print("La región seleccionada es inválida.")
else:
    print("No se seleccionó una región válida.")
