# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 02:22:41 2025

@author: addi_
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
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
tamano_ventana_movil = 3
TAMANO_VENTANA_ML = 5
# --- ¡NUEVO! UMBRAL DE ALERTA PARA LA IA ---
# ¿Qué valor predicho por la IA consideramos una "alerta"?
# ¡Ajusta este valor basándote en tu gráfica anterior! (ej. el 80% del pico)
UMBRAL_ALERTA_ML = 2000 

# --- FASES 1 Y 2 (Recolección y Suavizado) ---
# (Estas fases son idénticas al script anterior, las omito por brevedad)
# ... (imaginemos que el código de Fases 1 y 2 está aquí) ...
# ... (y que ya tenemos la variable 'areas_suavizadas') ...

fotogramas = []
areas_detectadas = []
if not os.path.isdir(ruta_carpeta):
    print(f"❌ ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    print(f"Iniciando Fase 1: Recolección de datos...")
    lista_archivos = sorted(os.listdir(ruta_carpeta))
    for contador_fotograma, nombre_archivo in enumerate(lista_archivos):
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            area_actual = analizar_imagen(ruta_completa)
            fotogramas.append(contador_fotograma)
            areas_detectadas.append(area_actual)
    print(f"✅ Recolección completa. Se procesaron {len(fotogramas)} fotogramas.")

    if fotogramas:
        series_areas = pd.Series(areas_detectadas)
        areas_suavizadas = series_areas.rolling(window=tamano_ventana_movil, min_periods=1).mean()
        
        # --- FASE 3: MACHINE LEARNING (PREDICCIÓN) ---
        print("\nIniciando Fase 3: Preparación de datos para ML...")
        datos_ml = areas_suavizadas.values
        X, y = crear_ventanas(datos_ml, TAMANO_VENTANA_ML)
        
        if len(X) < 20:
            print("No hay suficientes datos para entrenar un modelo.")
        else:
            limite_split = int(len(X) * 0.8)
            X_train, y_train = X[:limite_split], y[:limite_split]
            X_test, y_test   = X[limite_split:], y[limite_split:]
            print(f"Datos preparados: Entrenando con {len(X_train)} muestras, probando con {len(X_test)}.")

            modelo = LinearRegression()
            modelo.fit(X_train, y_train)
            
            # --- ¡AÑADE ESTAS DOS LÍNEAS! ---
            import joblib
            joblib.dump(modelo, 'predictor_llamaradas.pkl') 
            # ---------------------------------
            
            print(f"\n✅ ¡Modelo entrenado Y GUARDADO en 'predictor_llamaradas.pkl'!")
            
            predicciones = modelo.predict(X_test)
# ... (resto del script) ...
            predicciones = modelo.predict(X_test)
            error = np.sqrt(mean_squared_error(y_test, predicciones))
            print(f"\n✅ ¡Modelo entrenado! Error (RMSE): {error:.2f} píxeles.")
            
            # --- ¡NUEVO! FASE 4: SIMULACIÓN DE ALERTA PREDICTIVA ---
            print(f"\nIniciando Fase 4: Buscando alertas predictivas (Umbral > {UMBRAL_ALERTA_ML} px)...")
            alerta_ml_activa = False
            puntos_alerta_ml_x = []
            puntos_alerta_ml_y = []

            # Iteramos sobre las predicciones que hizo el modelo
            for i in range(len(predicciones)):
                prediccion_actual = predicciones[i]
                
                # El índice de tiempo real para esta predicción
                indice_tiempo = limite_split + TAMANO_VENTANA_ML + i 
                
                if prediccion_actual > UMBRAL_ALERTA_ML and not alerta_ml_activa:
                    print(f"\n🚨 ¡¡ALERTA PREDICTIVA DE ML!! 🚨")
                    print(f"   En el fotograma: Nº {indice_tiempo}")
                    print(f"   ¡El modelo predijo un área de {prediccion_actual:.0f} píxeles!")
                    
                    alerta_ml_activa = True
                    puntos_alerta_ml_x.append(indice_tiempo)
                    # Guardamos el valor REAL para ver qué tan acertada fue
                    puntos_alerta_ml_y.append(y_test[i]) 
            
                elif prediccion_actual < UMBRAL_ALERTA_ML and alerta_ml_activa:
                    print(f"-> Predicción de ML por debajo del umbral. Fin del evento.")
                    alerta_ml_activa = False

            # --- FASE 5: GRAFICACIÓN (con Alertas de ML) ---
            print("\nGenerando gráfica final con alertas predictivas...")
            plt.figure(figsize=(15, 7))
            
            # Datos reales (suavizados)
            plt.plot(fotogramas, areas_suavizadas, label='Datos Reales (Suavizados)', color='blue', alpha=0.8)
            
            # Eje X para las predicciones
            eje_x_predicciones = np.arange(limite_split + TAMANO_VENTANA_ML, len(areas_suavizadas))
            
            # Predicciones del modelo
            plt.plot(eje_x_predicciones, predicciones, label='Predicciones del Modelo (ML)', color='red', linestyle='--', linewidth=2)
            
            # Línea de división
            plt.axvline(x=limite_split + TAMANO_VENTANA_ML - 1, color='green', linestyle=':', label='Inicio de Pruebas')
            
            # ¡NUEVO! Marcar las alertas de ML en la gráfica
            plt.scatter(puntos_alerta_ml_x, puntos_alerta_ml_y, 
                        color='purple', 
                        marker='X', # Usamos una 'X'
                        s=200,      # Marcador grande
                        zorder=10,  # Ponerlo al frente
                        label='¡Alerta Predictiva de ML!')
            
            plt.title('Predicción de ML (Línea Roja) vs. Alertas (X Púrpura)')
            plt.xlabel('Número de Fotograma (Tiempo)')
            plt.ylabel('Área Detectada (en píxeles)')
            plt.grid(True)
            plt.legend()
            plt.show()
    else:
        print("No se procesaron fotogramas.")