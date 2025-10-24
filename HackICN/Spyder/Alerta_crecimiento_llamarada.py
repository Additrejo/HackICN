# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 01:12:59 2025

@author: addi_
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

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
                area_maxima = area
                
    return area_maxima

# --- BUCLE PRINCIPAL DE PROCESAMIENTO ---

# 1. Apunta a la carpeta donde guardaste los fotogramas
ruta_carpeta = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo"

# 2. --- ¡NUEVOS PARÁMETROS DE ALERTA! ---
# ¿Qué tan grande debe ser un área para que nos importe?
umbral_deteccion = 500 # Similar a tu area_minima
# ¿Cuánto debe crecer para disparar una alerta? (2.0 = 200% = se duplicó)
umbral_crecimiento = 2.0 

# 3. Variables para guardar el estado y los datos
area_anterior = 0
alerta_activa = False # Para no disparar 100 alertas por el mismo evento
fotogramas = []
areas_detectadas = []
# Listas para guardar los puntos de la gráfica donde hubo alertas
puntos_alerta_x = []
puntos_alerta_y = []

if not os.path.isdir(ruta_carpeta):
    print(f"ERROR: La carpeta especificada no existe: {ruta_carpeta}")
else:
    print(f"Iniciando monitoreo de alertas en: {ruta_carpeta}\n")
    lista_archivos = sorted(os.listdir(ruta_carpeta))
    
    for contador_fotograma, nombre_archivo in enumerate(lista_archivos):
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            
            # 4. Analizamos la imagen
            area_actual = analizar_imagen(ruta_completa)
            
            # 5. --- ¡LÓGICA DE ALERTA! ---
            # Si el área es significativa, creció rápido, y no hemos alertado ya...
            if (area_actual > umbral_deteccion and 
                area_anterior > 0 and 
                area_actual > (area_anterior * umbral_crecimiento) and 
                not alerta_activa):
                
                print(f"\n🚨 ¡¡ALERTA DE LLAMARADA!! 🚨")
                print(f"   En el fotograma: {nombre_archivo} (Nº {contador_fotograma})")
                print(f"   Crecimiento rápido detectado: de {int(area_anterior)} a {int(area_actual)} píxeles.")
                
                alerta_activa = True # Activamos la alerta
                # Guardamos el punto para la gráfica
                puntos_alerta_x.append(contador_fotograma)
                puntos_alerta_y.append(area_actual)

            # Si el evento termina (el área vuelve a ser pequeña), reseteamos la alerta
            elif area_actual < umbral_deteccion and alerta_activa:
                print(f"-> Evento finalizado en fotograma {contador_fotograma}.")
                alerta_activa = False
            
            # Guardamos datos para la gráfica
            fotogramas.append(contador_fotograma)
            areas_detectadas.append(area_actual)
            
            # Actualizamos el área anterior para la siguiente iteración
            area_anterior = area_actual

    print(f"\n Análisis completado. Se procesaron {len(fotogramas)} fotogramas.")

    # 6. Graficar los resultados
    if fotogramas:
        print("Generando gráfica de evolución con alertas...")
        plt.figure(figsize=(12, 6))
        
        # Dibujar la línea de evolución del área
        plt.plot(fotogramas, areas_detectadas, label='Área de la llamarada')
        
        # Dibujar los puntos de alerta
        plt.scatter(puntos_alerta_x, puntos_alerta_y, 
                    color='red', 
                    s=100, # Tamaño del marcador
                    zorder=5, # Ponerlo al frente
                    label='¡Alerta de Crecimiento Rápido!')
        
        plt.title('Evolución y Alertas de Llamaradas')
        plt.xlabel('Número de Fotograma (Tiempo)')
        plt.ylabel('Área Detectada (en píxeles)')
        plt.grid(True)
        plt.legend()
        plt.show() # Mostrará la gráfica en la pestaña "Plots"