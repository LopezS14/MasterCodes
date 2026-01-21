import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Image")

        # Variables de la clase
        self.img = None
        self.img_tk = None
        self.start_x = self.start_y = 0
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Cargar imagen
        self.img = cv2.imread("data/8 semanas/405 nm/RC1.JPG")

        # Redimensionar la imagen manteniendo la relación de aspecto
        (h, w) = self.img.shape[:2]
        new_width = 400
        aspect_ratio = h / w
        new_height = int(new_width * aspect_ratio)
        self.resized_img = cv2.resize(self.img, (new_width, new_height))
        self.img_pil = Image.fromarray(cv2.cvtColor(self.resized_img, cv2.COLOR_BGR2RGB))
        self.img_tk = ImageTk.PhotoImage(self.img_pil)

        # Mostrar la imagen redimensionada en el canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Variables para la selección libre
        self.points = []

        # Agregar eventos de mouse
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        """Detectar cuando el usuario presiona el botón izquierdo del ratón para comenzar a dibujar."""
        self.points = [(event.x, event.y)]  # Iniciar los puntos de la selección

    def on_mouse_drag(self, event):
        """Actualizar la selección libre mientras el usuario mueve el mouse."""
        self.points.append((event.x, event.y))

        # Limpiar el canvas y redibujar la imagen
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Dibujar la forma de la selección libre
        if len(self.points) > 1:
            self.canvas.create_line(self.points[-2], self.points[-1], fill="red", width=2)

    def on_button_release(self, event):
        """Recortar la imagen cuando el usuario suelta el botón del ratón."""
        if len(self.points) > 2:
            self.points.append((event.x, event.y))  # Finalizar la forma cerrada
            self.crop_image(self.points)

    def crop_image(self, points):
        """Recortar la imagen con una forma libre y mostrarla en el canvas."""
        # Crear una máscara negra del mismo tamaño que la imagen redimensionada
        mask = np.zeros(self.resized_img.shape[:2], dtype=np.uint8)

        # Convertir la lista de puntos en un array para usar cv2.fillPoly
        points_np = np.array([points], dtype=np.int32)

        # Rellenar la máscara con el polígono
        cv2.fillPoly(mask, points_np, 255)

        # Aplicar la máscara a la imagen original
        masked_img = cv2.bitwise_and(self.resized_img, self.resized_img, mask=mask)

        # Encontrar el área mínima de recorte
        x, y, w, h = cv2.boundingRect(points_np)
        cropped_img = masked_img[y:y+h, x:x+w]

        # Si el recorte está vacío, no guardar nada
        if cropped_img.size == 0:
            messagebox.showerror("Error", "No se pudo recortar la imagen. Intenta nuevamente.")
            return

        # Convertir la imagen recortada a formato PIL para mostrarla en el canvas
        masked_pil = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
        self.img_tk = ImageTk.PhotoImage(masked_pil)

        # Limpiar el canvas y mostrar la imagen recortada
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Crear carpeta si no existe
        if not os.path.exists('segmentacion'):
            os.makedirs('segmentacion')

        # Guardar la imagen recortada
        save_path = 'segmentacion/Azul R2.jpg'
        cv2.imwrite(save_path, cropped_img)
        print(f"Imagen guardada correctamente en {save_path}")

# Configurar la ventana Tkinter
root = tk.Tk()
app = ImageCropperApp(root)
root.mainloop()
