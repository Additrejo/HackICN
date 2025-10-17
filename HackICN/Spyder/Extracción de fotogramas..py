# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 23:25:33 2025

@author: addi_
"""

import cv2
import os

def extraer_fotogramas(ruta_del_video, carpeta_de_salida, intervalo_segundos=1):
    """
    Extrae fotogramas de un video a un intervalo de segundos especificado.
    
    :param ruta_del_video: La ruta al archivo de video (ej. "C:/videos/mi_video.mp4").
    :param carpeta_de_salida: La carpeta donde se guardarán las imágenes.
    :param intervalo_segundos: El intervalo en segundos para capturar un fotograma.
    """
    
    # 1. Comprobar si el video existe
    if not os.path.exists(ruta_del_video):
        print(f" ERROR: El archivo de video no se encontró en: {ruta_del_video}")
        return

    # 2. Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_de_salida):
        os.makedirs(carpeta_de_salida)
        print(f" Carpeta creada en: {carpeta_de_salida}")

    # 3. Abrir el archivo de video con OpenCV
    video = cv2.VideoCapture(ruta_del_video)
    
    # Obtener la tasa de fotogramas por segundo (fps) del video
    fps = video.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print(" ERROR: No se pudo obtener el FPS del video. Usando valor por defecto de 30.")
        fps = 30

    # Calcular cada cuántos fotogramas debemos guardar una imagen
    intervalo_fotogramas = int(fps * intervalo_segundos)
    
    contador_fotogramas = 0
    imagenes_guardadas = 0
    
    print(f"Iniciando extracción... (FPS: {fps:.2f}, guardando un fotograma cada {intervalo_fotogramas} frames)")

    while True:
        # 4. Leer el siguiente fotograma del video
        exito, fotograma = video.read()
        
        # Si 'exito' es False, significa que hemos llegado al final del video
        if not exito:
            break
        
        # 5. Comprobar si este es el fotograma que debemos guardar
        if contador_fotogramas % intervalo_fotogramas == 0:
            # Construir el nombre del archivo para la imagen
            nombre_archivo = os.path.join(carpeta_de_salida, f"fotograma_{imagenes_guardadas+1}.jpg")
            
            # Guardar el fotograma como un archivo JPG
            cv2.imwrite(nombre_archivo, fotograma)
            imagenes_guardadas += 1
        
        contador_fotogramas += 1

    # 6. Liberar el objeto de video
    video.release()
    print(f"\n Proceso completado. Se guardaron {imagenes_guardadas} imágenes en '{carpeta_de_salida}'.")


# --- ¡CONFIGURA TUS RUTAS AQUÍ! ---
# 1. Escribe la ruta donde guardaste tu video
ruta_video = r"C:\Users\addi_\Downloads\HackICN\Solarflare\SFVideo\SFVideo.mp4"

# 2. Escribe la ruta de la carpeta donde quieres guardar las imágenes
carpeta_salida = r"C:\Users\addi_\Downloads\HackICN\Solarflare\SFVideo"

# 3. Define cada cuántos segundos quieres una foto (ej. 0.5 para 2 fotos por segundo)
intervalo = 1 # Guardar una foto cada 2 segundos

# Ejecutar la función
extraer_fotogramas(ruta_video, carpeta_salida, intervalo)