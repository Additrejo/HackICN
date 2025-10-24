# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 00:34:15 2025

@author: addi_
"""

import cv2
import numpy as np
import os # ¡Importamos la librería os!

def analizar_imagen(ruta_imagen, area_minima=500, umbral=170):
    """
    Toma la ruta de una imagen, la procesa y devuelve una lista de las
    llamaradas detectadas con sus datos.
    """
    img = cv2.imread(ruta_imagen)
    resultados_imagen = []

    if img is None:
        print(f"Advertencia: No se pudo leer la imagen {ruta_imagen}, se omitirá.")
        return resultados_imagen

    # Preprocesamiento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, mascara = cv2.threshold(gray, umbral, 255, cv2.THRESH_BINARY)
    
    # Encontrar y analizar contornos
    contornos, jerarquia = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area > area_minima:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # Guardar los datos de esta detección
                resultados_imagen.append({
                    'area': area,
                    'centroide': (cX, cY)
                })
    return resultados_imagen

# --- BUCLE PRINCIPAL DE PROCESAMIENTO ---

# 1. Define la ruta a tu carpeta de imágenes
# ¡¡Asegúrate de que esta carpeta exista y tenga imágenes!!
ruta_carpeta = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo"

# 2. Almacenaremos todos los resultados aquí
todos_los_resultados = {}

if not os.path.exists(ruta_carpeta):
    print(f" ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    # 3. Recorrer cada archivo en la carpeta
    for nombre_archivo in os.listdir(ruta_carpeta):
        # Nos aseguramos de procesar solo archivos de imagen comunes
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.tif')):
            # Construir la ruta completa al archivo
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            
            print(f"Procesando: {nombre_archivo}...")
            
            # 4. Analizar la imagen y guardar el resultado
            datos_llamaradas = analizar_imagen(ruta_completa)
            if datos_llamaradas: # Solo agregar si se detectó algo
                todos_los_resultados[nombre_archivo] = datos_llamaradas

# 5. Imprimir un resumen final
print("\n--- RESUMEN DEL PROCESAMIENTO ---")
if not todos_los_resultados:
    print("No se detectaron llamaradas en ninguna imagen.")
else:
    for archivo, data in todos_los_resultados.items():
        print(f"\nArchivo: {archivo}")
        for i, deteccion in enumerate(data):
            print(f"  - Detección {i+1}: Área={int(deteccion['area'])}, Centroide={deteccion['centroide']}")