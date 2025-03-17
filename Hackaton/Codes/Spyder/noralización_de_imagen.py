import cv2
import numpy as np

# Cargar imagen en escala de grises
imagen = cv2.imread("C:/Users/addi_/Downloads/Hackaton/imagenes/Solarflare.jpg", cv2.IMREAD_GRAYSCALE)

# Normalización Min-Max a rango [0, 1]
imagen_normalizada = imagen.astype(np.float32) / 255.0

cv2.imshow("Imagen Normalizada", imagen_normalizada)
cv2.waitKey(0)
cv2.destroyAllWindows()
