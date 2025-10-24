# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 00:49:56 2025

@author: addi_
"""

import cv2
import numpy as np
import os # ¡Importante para leer carpetas!

def analizar_imagen(ruta_imagen, area_minima=500, umbral=170):
    """
    Toma la ruta de una imagen, la procesa y devuelve una lista de las
    llamaradas detectadas con sus datos (área y centroide).
    """
    img = cv2.imread(ruta_imagen)
    resultados_de_la_imagen = []

    if img is None:
        print(f"-> Advertencia: No se pudo leer la imagen {os.path.basename(ruta_imagen)}, se omitirá.")
        return resultados_de_la_imagen

    # 1. Preprocesamiento de la imagen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # --- ¡Ajusta este umbral si es necesario! ---
    ret, mascara = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    
    # 2. Encontrar y analizar los contornos
    contornos, jerarquia = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area > area_minima:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # Guardamos los datos de esta detección
                resultados_de_la_imagen.append({
                    'area': area,
                    'centroide': (cX, cY)
                })
    return resultados_de_la_imagen

# --- BUCLE PRINCIPAL DE PROCESAMIENTO ---

# 1. ¡¡MODIFICA ESTA LÍNEA!!
#    Apunta a la carpeta donde guardaste los fotogramas del video.
#    (Debe ser la misma que tu 'carpeta_salida' del script anterior)
ruta_carpeta = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo" # <-- ¡CÁMBIA ESTO!

# 2. Almacenaremos todos los resultados aquí
todos_los_resultados = {}
archivos_procesados = []

if not os.path.isdir(ruta_carpeta):
    print(f" ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    print(f"Iniciando análisis en la carpeta: {ruta_carpeta}\n")
    # 3. Recorremos cada archivo dentro de la carpeta
    # Ordenamos los archivos para mantener (en parte) el orden del video
    # Nota: Esto ordena alfabéticamente (ej. frame_1, frame_10, frame_2)
    # Para un orden numérico perfecto se requiere un 'sort' más avanzado,
    # pero para esto es suficiente.
    lista_archivos_ordenada = sorted(os.listdir(ruta_carpeta))
    
    for nombre_archivo in lista_archivos_ordenada:
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            
            # 4. Analizamos la imagen y guardamos el resultado
            datos_llamaradas = analizar_imagen(ruta_completa)
            
            # Guardamos el resultado (incluso si está vacío) para mantener la secuencia
            todos_los_resultados[nombre_archivo] = datos_llamaradas
            archivos_procesados.append(nombre_archivo)

# 5. Imprimimos un resumen final
print("\n--- RESUMEN FINAL DEL PROCESAMIENTO ---")
if not todos_los_resultados:
    print("No se detectaron llamaradas en ninguna de las imágenes procesadas.")
else:
    print(f"Se procesaron {len(archivos_procesados)} fotogramas.")
    detecciones_totales = sum(len(v) for v in todos_los_resultados.values())
    print(f"Se encontraron {detecciones_totales} detecciones en total.")
    
    # Imprimir los primeros 10 resultados para verificar
    print("\nMostrando resultados de los primeros fotogramas:")
    for i in range(min(10, len(archivos_procesados))):
        archivo = archivos_procesados[i]
        data = todos_los_resultados[archivo]
        if data:
            print(f"  Archivo: {archivo} -> {len(data)} detecciones")
        else:
            print(f"  Archivo: {archivo} -> Sin detecciones")