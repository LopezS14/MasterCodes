import cv2
import numpy as np
import imutils
image = cv2.imread('data/Blanco R1.jpg',0)
image = imutils.resize(image, width=400)#Se puede omitir esta línea
_, Toz = cv2.threshold(image, 210, 255, cv2.THRESH_TOZERO)
_, TozInv = cv2.threshold(image, 210, 255, cv2.THRESH_TOZERO_INV)
cv2.imshow('Tipos: Tozero - Tozero Inv',np.hstack([Toz,TozInv]))
cv2.waitKey(0)
cv2.destroyAllWindows()