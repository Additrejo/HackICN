# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 02:56:39 2025

@author: addi_
"""

import cv2
import numpy as np
import pandas as pd
import joblib
from collections import deque

# --- PARÁMETROS GLOBALES (Ajústalos) ---
AREA_MINIMA = 500         # Área mínima para detectar una llamarada
UMBRAL_CV = 170           # Umbral de brillo (0-255)
TAMANO_VENTANA_MOVIL = 3  # Para suavizar los datos (debe ser el mismo que usaste para entrenar)
TAMANO_VENTANA_ML = 5       # Ventana de entrada del modelo (debe ser el mismo)
UMBRAL_ALERTA_ML = 2000   # Umbral de PREDICCIÓN para disparar la alerta

def analizar_imagen_con_recuadro(frame):
    """
    Analiza un fotograma, encuentra la llamarada más grande
    y devuelve su área y su recuadro (bounding box).
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, mascara = cv2.threshold(gray, UMBRAL_CV, 255, cv2.THRESH_BINARY)
    
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    area_maxima = 0
    recuadro = None # (x, y, w, h)
    
    if len(contornos) > 0:
        # Encontrar el contorno más grande
        c_max = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(c_max)
        
        if area > AREA_MINIMA:
            area_maxima = area
            # Calcular el recuadro (bounding box)
            recuadro = cv2.boundingRect(c_max) 
            
    return area_maxima, recuadro

# --- 1. CARGA DEL MODELO Y PREPARACIÓN ---

print("Cargando modelo de IA desde 'predictor_llamaradas.pkl'...")
try:
    modelo = joblib.load('predictor_llamaradas.pkl')
except FileNotFoundError:
    print(" ERROR: No se encontró el archivo 'predictor_llamaradas.pkl'.")
    print("Asegúrate de ejecutar el Paso 12.A para guardarlo primero.")
    exit()

print("¡Modelo cargado!")

# ¡MODIFICA ESTA RUTA! Usa un video NUEVO que el modelo no haya visto.
ruta_video_nuevo = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo/SFVideo.mp4"
video = cv2.VideoCapture(ruta_video_nuevo)

if not video.isOpened():
    print(f" ERROR: No se pudo abrir el video en: {ruta_video_nuevo}")
    exit()

# Usamos una 'deque' para guardar eficientemente el historial de datos
# Necesita guardar suficientes datos para la media móvil y la ventana de ML
historial_areas = deque(maxlen=TAMANO_VENTANA_MOVIL + TAMANO_VENTANA_ML)
alerta_activa = False

# --- 2. BUCLE DE SIMULACIÓN EN TIEMPO REAL ---

while True:
    exito, frame = video.read()
    if not exito:
        print("Fin del video.")
        break # Salir del bucle si se acaba el video

    # 2a. Detección con OpenCV
    area_actual, recuadro = analizar_imagen_con_recuadro(frame)
    
    # 2b. Dibujar el Recuadro (si se detectó algo)
    if recuadro is not None:
        x, y, w, h = recuadro
        # Dibuja el recuadro verde
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Area: {int(area_actual)}", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 2c. Lógica de Predicción
    historial_areas.append(area_actual)

    # No podemos predecir hasta que tengamos suficientes datos históricos
    if len(historial_areas) < TAMANO_VENTANA_MOVIL + TAMANO_VENTANA_ML -1:
        cv2.imshow("Simulacion en Vivo - (Cargando datos...)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue # Seguir al siguiente fotograma

    # 2d. Preparar datos para el modelo
    # 1. Suavizar el historial reciente
    series_suavizada = pd.Series(historial_areas).rolling(window=TAMANO_VENTANA_MOVIL).mean()
    # 2. Tomar los últimos N puntos para la predicción
    datos_para_predecir = series_suavizada.values[-TAMANO_VENTANA_ML:]
    
    # 2e. ¡HACER LA PREDICCIÓN!
    prediccion = modelo.predict(datos_para_predecir.reshape(1, -1))[0]
    
    # 2f. Lógica de Alerta
    if prediccion > UMBRAL_ALERTA_ML and not alerta_activa:
        alerta_activa = True
        print(f"🚨 ¡¡ALERTA PREDICTIVA!! El modelo predice un área de {prediccion:.0f} píxeles. 🚨")
    elif prediccion < UMBRAL_ALERTA_ML and alerta_activa:
        alerta_activa = False # Resetear la alerta

    # 2g. Dibujar la alerta en pantalla
    if alerta_activa:
        cv2.rectangle(frame, (10, 10), (frame.shape[1] - 10, 60), (0, 0, 255), -1)
        cv2.putText(frame, f"ALERTA PREDICTIVA! (Pred: {prediccion:.0f} px)", (20, 45), 
                    cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 2)

    # 2h. Mostrar el fotograma final
    cv2.imshow('Simulacion en Vivo', frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 3. LIMPIEZA ---
video.release()
cv2.destroyAllWindows()