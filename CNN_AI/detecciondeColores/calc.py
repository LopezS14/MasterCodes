import cv2
import numpy as np

# Variables globales
dibujando = False
puntos = []
area = None
imagen_resized = None
scale_factor = 1.0

def dibujar_libre(event, x, y, flags, param):
    global puntos, dibujando, imagen_resized, scale_factor, area

    if event == cv2.EVENT_LBUTTONDOWN:
        dibujando = True
        puntos = [(x, y)]  # Iniciar nuevo trazo

    elif event == cv2.EVENT_MOUSEMOVE:
        if dibujando:
            puntos.append((x, y))  # Agregar puntos mientras se mueve
            # Dibujar línea temporal
            temp_img = imagen_resized.copy()
            if len(puntos) > 1:
                cv2.polylines(temp_img, [np.array(puntos)], False, (0,255,0), 2)
            cv2.imshow('Dibujo Libre (500px)', temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        dibujando = False
        if len(puntos) > 2:  # Calcular área solo si hay suficientes puntos
            # Cerrar el contorno automáticamente
            pts = np.array(puntos + [puntos[0]], dtype=np.int32)
            
            # Calcular área (versión redimensionada)
            area_redim = cv2.contourArea(pts)
            # Escalar al área original
            area = area_redim / (scale_factor ** 2)
            
            # Dibujar resultado final
            cv2.polylines(imagen_resized, [pts], True, (0,255,0), 2)
            texto = f'Área: {area:,.2f} px²'
            cv2.putText(imagen_resized, texto, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.imshow('Dibujo Libre (500px)', imagen_resized)
            puntos = []  # Reiniciar

# Cargar y redimensionar imagen
imagen_original = cv2.imread('data/2 semanas/455nm/Copy of Azul R2(1).JPG')
if imagen_original is None:
    print("Error: No se pudo cargar la imagen.")
    exit()

# Redimensionar a máximo 500px manteniendo relación de aspecto
h, w = imagen_original.shape[:2]
max_dim = max(h, w)
scale_factor = 500 / max_dim
nuevo_w = int(w * scale_factor)
nuevo_h = int(h * scale_factor)
imagen_resized = cv2.resize(imagen_original, (nuevo_w, nuevo_h))

# Configurar ventana y eventos
cv2.namedWindow('Dibujo Libre (500px)')
cv2.setMouseCallback('Dibujo Libre (500px)', dibujar_libre)

print("Instrucciones:")
print("1. Click izquierdo + arrastrar: Dibujar forma libre")
print("2. Suelta el click para calcular el área")
print("Tecla 'r': Reiniciar | Tecla 'q': Salir")

while True:
    cv2.imshow('Dibujo Libre (500px)', imagen_resized)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('r'):  # Reiniciar
        puntos = []
        area = None
        imagen_resized = cv2.resize(imagen_original, (nuevo_w, nuevo_h))
        
    elif key == ord('q'):  # Salir
        break

cv2.destroyAllWindows()