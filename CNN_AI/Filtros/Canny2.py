import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectar_bordes(imagen_path):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print("Error: No se pudo cargar la imagen.")
        return
    
    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque Gaussiano
    desenfoque = cv2.GaussianBlur(gris, (3, 3), 1)
    
    # Aplicar Canny para detectar bordes
    bordes = cv2.Canny(desenfoque, 50, 150)

    # Hacer los bordes más gruesos usando dilatación
    kernel = np.ones((3,3), np.uint8)  # Puedes probar con (5,5) para más grosor
    bordes_gruesos = cv2.dilate(bordes, kernel, iterations=1)

    # Convertir la imagen original de BGR a RGB para mostrarla correctamente
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Mostrar la imagen original y la imagen con bordes detectados
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.imshow(imagen_rgb)
    plt.title('Imagen Original')
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.imshow(bordes_gruesos, cmap='gray')  # Fondo negro, bordes blancos gruesos
    plt.title('Bordes Canny Gruesos')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# Ruta de la imagen de prueba
imagen_path = "data/Azul R2.JPG"
detectar_bordes(imagen_path)
