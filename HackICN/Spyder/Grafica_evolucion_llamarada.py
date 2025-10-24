# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 00:59:54 2025

@author: addi_
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt # ¡Importamos Matplotlib!

def analizar_imagen(ruta_imagen, area_minima=500, umbral=170):
    """
    Analiza una imagen y devuelve el ÁREA MÁXIMA de la llamarada encontrada.
    """
    img = cv2.imread(ruta_imagen)
    if img is None:
        return 0 # Devolvemos 0 si no hay imagen

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, mascara = cv2.threshold(gray, umbral, 255, cv2.THRESH_BINARY)
    
    contornos, jerarquia = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    area_maxima = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > area_minima:
            if area > area_maxima:
                area_maxima = area # Nos quedamos solo con el área más grande
                
    return area_maxima

# --- BUCLE PRINCIPAL DE PROCESAMIENTO ---

# 1. Apunta a la carpeta dondse guardaste los fotogramas del video
ruta_carpeta = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo"

# 2. Listas para guardar nuestros datos para la gráfica
# Eje X: El número de fotograma
fotogramas = []
# Eje Y: El área máxima detectada en ese fotograma
areas_detectadas = []

if not os.path.isdir(ruta_carpeta):
    print(f" ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    print(f"Iniciando análisis para graficar: {ruta_carpeta}\n")
    
    lista_archivos = sorted(os.listdir(ruta_carpeta))
    
    contador_fotograma = 0
    for nombre_archivo in lista_archivos:
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            
            # 3. Analizamos la imagen y obtenemos el área máxima
            area_max = analizar_imagen(ruta_completa)
            
            # 4. Guardamos los datos en nuestras listas
            fotogramas.append(contador_fotograma)
            areas_detectadas.append(area_max)
            
            contador_fotograma += 1
            if contador_fotograma % 50 == 0:
                print(f"Procesados {contador_fotograma} fotogramas...")

    print(f"\n Análisis completado. Se procesaron {contador_fotograma} fotogramas.")

    # 5. --- ¡NUEVO! --- Graficar los resultados con Matplotlib
    if fotogramas:
        print("Generando gráfica de evolución...")
        plt.figure(figsize=(12, 6))
        plt.plot(fotogramas, areas_detectadas)
        plt.title('Evolución del Área de la Llamarada a lo largo del Tiempo')
        plt.xlabel('Número de Fotograma (Tiempo)')
        plt.ylabel('Área Detectada (en píxeles)')
        plt.grid(True)
        plt.show() # ¡Esto abrirá la ventana con la gráfica!
    else:
        print("No se procesaron fotogramas, no se puede graficar.")