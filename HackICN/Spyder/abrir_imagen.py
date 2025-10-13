# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 22:52:56 2025

@author: addiTrejo
"""

import cv2

# Cargar una imagen desde tu computadora
# Asegúrate de que la ruta al archivo sea correcta
img = cv2.imread('C:/Users/addi_/Downloads/HackICN/Solarflare/SDO-solarflare.jpg')

# img ahora aparecerá en tu Explorador de Variables. ¡Inspecciónala!

# Mostrar la imagen en una ventana nueva de OpenCV
cv2.imshow('Importar Imagen', img)

# Espera a que se presione una tecla para cerrar la ventana
# Esta línea es crucial para que la ventana no se cierre al instante
cv2.waitKey(0)

# Cierra todas las ventanas creadas por OpenCV
cv2.destroyAllWindows()