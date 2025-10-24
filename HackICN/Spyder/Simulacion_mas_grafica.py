import cv2
import numpy as np
import pandas as pd
import joblib
from collections import deque

# --- PARÁMETROS GLOBALES ---
AREA_MINIMA = 500
UMBRAL_CV = 170
TAMANO_VENTANA_MOVIL = 3
TAMANO_VENTANA_ML = 5
UMBRAL_ALERTA_ML = 2000
ANCHO_PANTALLA_DESEADO = 800 # Ventana de 800px

# --- Función de Detección (la misma de antes) ---
def analizar_imagen_con_recuadro(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, mascara = cv2.threshold(gray, UMBRAL_CV, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_maxima = 0
    recuadro = None
    if len(contornos) > 0:
        c_max = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(c_max)
        if area > AREA_MINIMA:
            area_maxima = area
            recuadro = cv2.boundingRect(c_max)
    return area_maxima, recuadro

# --- Función para DIBUJAR LA GRÁFICA ---
def dibujar_grafica_mejorada(frame_grafica, historial_datos, max_area_vista, puntos_de_alerta):
    h, w, _ = frame_grafica.shape
    frame_grafica.fill(255) # Fondo blanco
    color_grid = (220, 220, 220)
    color_texto = (0, 0, 0)
    color_linea_real = (255, 0, 0) # Azul (BGR)
    color_alerta = (128, 0, 128) # Púrpura

    # Dibujar Cuadrícula
    for i in range(1, 5):
        y = int(h * (i / 5)); cv2.line(frame_grafica, (0, y), (w, y), color_grid, 1)
        x = int(w * (i / 5)); cv2.line(frame_grafica, (x, 0), (x, h), color_grid, 1)

    # --- ¡CAMBIO! ETIQUETAS DE EJES ACTUALIZADAS ---
    # (Se omiten tildes por compatibilidad con cv2.putText)
    cv2.putText(frame_grafica, "Numero de fotograma - Tiempo", (w - 300, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 1)
    cv2.putText(frame_grafica, "Area detectada en pixeles", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 1)
    # --------------------------------------------------

    if len(historial_datos) < 2:
        return frame_grafica 

    puntos_reales = []
    max_val = max(max_area_vista, 1)
    
    for i, valor in enumerate(historial_datos):
        x = int(i * (w / len(historial_datos)))
        y = int(h - (valor / max_val) * (h * 0.9))
        puntos_reales.append([x, y])
    
    cv2.polylines(frame_grafica, [np.array(puntos_reales)], isClosed=False, color=color_linea_real, thickness=2)
    cv2.line(frame_grafica, (puntos_reales[-1][0], 0), (puntos_reales[-1][0], h), (100, 100, 100), 1)
    cv2.putText(frame_grafica, f"Area (real): {historial_datos[-1]:.0f}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_texto, 2)

    # Dibujar los marcadores de alerta
    for punto in puntos_de_alerta:
        x_alerta = int(punto[0] * (w / len(historial_datos)))
        y_alerta = int(h - (punto[1] / max_val) * (h * 0.9))
        cv2.drawMarker(frame_grafica, (x_alerta, y_alerta), color_alerta, 
                       markerType=cv2.MARKER_TILTED_CROSS, markerSize=20, thickness=3)

    return frame_grafica

# --- 1. CARGA DEL MODELO Y PREPARACIÓN ---
print("Cargando modelo de IA 'predictor_llamaradas.pkl'...")
try:
    modelo = joblib.load('predictor_llamaradas.pkl')
except FileNotFoundError:
    print("❌ ERROR: No se encontró el archivo 'predictor_llamaradas.pkl'.")
    exit()

ruta_video_nuevo = r"C:/Users/addi_/Downloads/HackICN/Solarflare/SFVideo/SFVideo.mp4" # ¡MODIFICA ESTO!
video = cv2.VideoCapture(ruta_video_nuevo)

if not video.isOpened():
    print(f"❌ ERROR: No se pudo abrir el video en: {ruta_video_nuevo}")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

ancho_final = ancho * 2
lienzo_final = np.zeros((alto, ancho_final, 3), dtype=np.uint8)
frame_grafica = np.zeros((alto, ancho, 3), dtype=np.uint8)

video_salida = cv2.VideoWriter('simulacion_lado_a_lado.mp4', 
                               cv2.VideoWriter_fourcc(*'mp4v'), 
                               fps, (ancho_final, alto))

# Historial para la IA y la gráfica
historial_areas_raw = deque(maxlen=TAMANO_VENTANA_MOVIL + TAMANO_VENTANA_ML)
historial_completo_suavizado = [] 
historial_puntos_alerta = [] 
max_area_vista = 1 
alerta_activa = False
fotograma_actual = 0

# --- 2. BUCLE DE SIMULACIÓN EN TIEMPO REAL ---
print("Iniciando simulación... Presiona 'q' para salir.")
while True:
    exito, frame = video.read()
    if not exito:
        break 

    fotograma_actual += 1

    # --- LADO IZQUIERDO: Detección en Video ---
    area_actual, recuadro = analizar_imagen_con_recuadro(frame)
    if recuadro:
        x, y, w, h = recuadro
        color_deteccion = (0, 0, 255) # Rojo (BGR)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color_deteccion, 2)
        cv2.putText(frame, f"Area: {int(area_actual)} px", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_deteccion, 2)

    # --- LÓGICA DE PREDICCIÓN (IA) ---
    historial_areas_raw.append(area_actual)
    prediccion = 0
    area_suavizada_actual = 0
    
    if len(historial_areas_raw) >= TAMANO_VENTANA_MOVIL:
        series_suavizada = pd.Series(historial_areas_raw).rolling(window=TAMANO_VENTANA_MOVIL).mean()
        area_suavizada_actual = series_suavizada.iloc[-1]
        historial_completo_suavizado.append(area_suavizada_actual)
        
        if area_suavizada_actual > max_area_vista:
            max_area_vista = area_suavizada_actual
        
        if len(series_suavizada) >= TAMANO_VENTANA_ML:
            datos_para_predecir = series_suavizada.values[-TAMANO_VENTANA_ML:]
            if not np.isnan(datos_para_predecir).any(): 
                prediccion = modelo.predict(datos_para_predecir.reshape(1, -1))[0]
    
    if prediccion > UMBRAL_ALERTA_ML and not alerta_activa:
        alerta_activa = True
        historial_puntos_alerta.append((fotograma_actual, area_suavizada_actual))
    elif prediccion < UMBRAL_ALERTA_ML and alerta_activa:
        alerta_activa = False

    # --- LADO DERECHO: Dibujo de Gráfica ---
    frame_grafica = dibujar_grafica_mejorada(frame_grafica, historial_completo_suavizado, 
                                            max_area_vista, historial_puntos_alerta)
    cv2.putText(frame_grafica, f"Prediccion: {prediccion:.0f}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 200), 2)

    if alerta_activa:
        texto_alerta = "!! ALERTA PREDICTIVA !!"
        cv2.putText(frame, texto_alerta, (30, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 0, 255), 2)
        cv2.putText(frame_grafica, texto_alerta, (30, 110), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 0, 255), 2)

    # --- ENSAMBLAJE FINAL ---
    lienzo_final[0:alto, 0:ancho] = frame
    lienzo_final[0:alto, ancho:ancho_final] = frame_grafica

    # Redimensionar la ventana para mostrar
    relacion_aspecto = alto / ancho_final
    alto_pantalla_deseado = int(ANCHO_PANTALLA_DESEADO * relacion_aspecto)
    
    lienzo_mostrado = cv2.resize(lienzo_final, (ANCHO_PANTALLA_DESEADO, alto_pantalla_deseado), 
                                 interpolation=cv2.INTER_AREA)

    cv2.imshow('Simulacion Lado-a-Lado (Presiona q para salir)', lienzo_mostrado)
    video_salida.write(lienzo_final) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 3. LIMPIEZA ---
video.release()
video_salida.release()
cv2.destroyAllWindows()
print("Simulación finalizada. Video guardado en 'simulacion_lado_a_lado.mp4'.")