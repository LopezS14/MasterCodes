import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('data/Azul R2.jpg')
cv2.imshow('test.jpg', img)
"None mascara de convolucion"
color = ('b','g','r')

for i, c in enumerate(color):
    hist = cv2.calcHist([img], [i], None, [255], [0, 255])
    plt.plot(hist, color = c)
    plt.ylim([0,256])
    plt.xlabel("cantidad de pixeles ", color='black')
    plt.ylabel("Nivel de intensidad", color='black')
    plt.title("Canales RGB hígado 365 nm ",color='black')


plt.show()


cv2.destroyAllWindows()