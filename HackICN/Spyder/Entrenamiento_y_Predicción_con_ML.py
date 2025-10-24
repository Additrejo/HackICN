# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 01:56:36 2025

@author: addi_
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
# --- ¡NUEVAS IMPORTACIONES PARA ML! ---
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def analizar_imagen(ruta_imagen, area_minima=500, umbral=170):
    """
    Analiza una imagen y devuelve el ÁREA MÁXIMA de la llamarada encontrada.
    """
    img = cv2.imread(ruta_imagen)
    if img is None:
        return 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, mascara = cv2.threshold(gray, umbral, 255, cv2.THRESH_BINARY)
    contornos, jerarquia = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_maxima = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > area_minima:
            if area > area_maxima:
                area_maxima = area
    return area_maxima

def crear_ventanas(datos, tamano_ventana):
    """
    Crea las "ventanas deslizantes" para el modelo de ML.
    X = [t-ventana, ..., t-1], y = [t]
    """
    X, y = [], []
    for i in range(len(datos) - tamano_ventana):
        X.append(datos[i:(i + tamano_ventana)])
        y.append(datos[i + tamano_ventana])
    return np.array(X), np.array(y)

# --- PARÁMETROS DE PROCESAMIENTO ---
ruta_carpeta = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo"
tamano_ventana_movil = 3 # Para suavizar la curva
TAMANO_VENTANA_ML = 5      # ¡NUEVO! Fotogramas pasados para predecir el futuro

# --- 1. FASE DE RECOLECCIÓN DE DATOS ---
fotogramas = []
areas_detectadas = [] # Lista para los datos crudos

if not os.path.isdir(ruta_carpeta):
    print(f" ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    print(f"Iniciando Fase 1: Recolección de datos...")
    lista_archivos = sorted(os.listdir(ruta_carpeta))
    
    for contador_fotograma, nombre_archivo in enumerate(lista_archivos):
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            area_actual = analizar_imagen(ruta_completa)
            fotogramas.append(contador_fotograma)
            areas_detectadas.append(area_actual)
            
    print(f" Recolección completa. Se procesaron {len(fotogramas)} fotogramas.")

    # --- 2. FASE DE SUAVIZADO DE DATOS ---
    if fotogramas:
        series_areas = pd.Series(areas_detectadas)
        areas_suavizadas = series_areas.rolling(window=tamano_ventana_movil, min_periods=1).mean()
        
        # --- 3. FASE DE MACHINE LEARNING (PREDICCIÓN) ---
        print("\nIniciando Fase 3: Preparación de datos para ML...")
        datos_ml = areas_suavizadas.values
        
        # 3a. Crear las "tarjetas de memoria" (X, y)
        X, y = crear_ventanas(datos_ml, TAMANO_VENTANA_ML)
        
        if len(X) < 20: # Necesitamos suficientes datos para entrenar y probar
            print("No hay suficientes datos para entrenar un modelo. Intenta con un video más largo.")
        else:
            # 3b. Dividir los datos (80% entrenamiento, 20% prueba)
            # ¡¡IMPORTANTE: En series de tiempo, NO barajamos los datos!!
            limite_split = int(len(X) * 0.8)
            
            X_train, y_train = X[:limite_split], y[:limite_split]
            X_test, y_test   = X[limite_split:], y[limite_split:]
            
            print(f"Datos preparados: Entrenando con {len(X_train)} muestras, probando con {len(X_test)}.")

            # 3c. Entrenar el modelo
            modelo = LinearRegression()
            modelo.fit(X_train, y_train)
            
            # 3d. Hacer predicciones en el conjunto de prueba
            predicciones = modelo.predict(X_test)
            
            # 3e. Evaluar el modelo
            error = np.sqrt(mean_squared_error(y_test, predicciones))
            print(f"\n ¡Modelo entrenado! Error (RMSE): {error:.2f} píxeles.")
            print("   (Esto es, en promedio, qué tan 'equivocado' está el modelo al predecir el área).")

            # --- 4. FASE DE GRAFICACIÓN (con Predicciones) ---
            print("\nGenerando gráfica final con predicciones...")
            plt.figure(figsize=(15, 7))
            
            # 4a. Eje X para las predicciones
            # (debe alinearse con la porción de 'test' de los datos)
            eje_x_predicciones = np.arange(limite_split + TAMANO_VENTANA_ML, len(areas_suavizadas))

            # 4b. Graficar la serie de datos completa (suavizada)
            plt.plot(fotogramas, areas_suavizadas, label='Datos Reales (Suavizados)', color='blue', alpha=0.8)
            
            # 4c. Graficar las predicciones del modelo
            plt.plot(eje_x_predicciones, predicciones, 
                     label='Predicciones del Modelo (ML)', 
                     color='red', 
                     linestyle='--', 
                     linewidth=2)
            
            # 4d. Añadir una línea vertical para ver dónde empieza la "prueba"
            plt.axvline(x=limite_split + TAMANO_VENTANA_ML - 1, color='green', linestyle=':', label='Inicio de Pruebas')
            
            plt.title('Predicción de ML (Línea Roja) vs. Datos Reales (Línea Azul)')
            plt.xlabel('Número de Fotograma (Tiempo)')
            plt.ylabel('Área Detectada (en píxeles)')
            plt.grid(True)
            plt.legend()
            plt.show()
    else:
        print("No se procesaron fotogramas.")