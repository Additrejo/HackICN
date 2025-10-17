# HackICN - Análisis de imágenes del Sol para identificar y predecir llamaradas solares

## Reto 1 - Llamaradas solares
Análisis de imágenes del Sol para identificar y predecir llamaradas solares

<img width="669" height="836" alt="image" src="https://github.com/user-attachments/assets/3a4aa3a6-2f86-4253-b44a-e68f6fe959bf" />



# Recursos.
Base de datos imagenes solares.
[NASA - Interactive Multi-Instrument Database of Solar Flares](https://data.nas.nasa.gov/helio/portals/solarflares/#url)

# Instalación: 

### **1. Clonar el repositorio.**
```Powershell
git clone https://github.com/NASA-IMPACT/Surya.git
cd Surya
```

### **2. Instalar el gestor de paquetes uv (opcional)(Windows).**
```Powershell
.\install_uv.ps1
```

<img width="362" height="102" alt="image" src="https://github.com/user-attachments/assets/4a177115-4aa0-4cce-b1eb-1c9def076a56" />

### **3. Verifcar si está instalado.**  
Abrir otra ventana de powershell y escribir el siguiente comando.
```Powershell
uv --version
```
<img width="264" height="42" alt="image" src="https://github.com/user-attachments/assets/98597ae6-3f38-4883-af5b-ef184dc84195" />

### **4. Configura el Entorno del Proyecto: El siguiente paso de la documentación es usar uv para instalar todas las librerías que el proyecto SURYA necesita. Ejecuta este comando:**

```Powershell
uv sync
```
Se instalarán  todas las librerías necesarias.  
<img width="516" height="130" alt="image" src="https://github.com/user-attachments/assets/a7558e56-48a3-4912-9a4c-73a316652b56" />

### **5. Activar el Entorno Virtual.**  
- Asegúrar de estar en la carpeta Surya.
- Ejecuta el siguiente comando para activar el entorno:  
```Powershell
.venv\Scripts\activate
```
<img width="362" height="32" alt="image" src="https://github.com/user-attachments/assets/4c24b956-1c34-4c5b-8992-5ea56ed5cd18" />  

# 🧪 Verificar la instalación

- [] probar modelo en computadora del laboratorio.

---

## OPENCV Spyder.
Instalar OpenCV.  
Si ya tienes una distribución de Python como Anaconda, lo más probable es que ya tengas Spyder instalado. Solo necesitas instalar OpenCV.

- Abre una terminal (o la "Anaconda Prompt" si usas Anaconda).
- Instala OpenCV con pip. El paquete que necesitas se llama opencv-python.
```Powershell
pip install opencv-python
```

## Plan maestro:

## 1. Identificación de Llamaradas (Detección) 
El objetivo es encontrar las zonas de la imagen que corresponden a una llamarada, que son esencialmente regiones con un brillo anómalo y repentino.

**Carga y preprocesamiento:** Cargar las imágenes del Sol. Como las llamaradas son fenómenos muy brillantes, un buen primer paso es convertir la imagen a escala de grises y aplicar filtros para reducir el ruido, como un filtro Gaussiano (cv2.GaussianBlur).

**Detección de zonas brillantes (Thresholding):** Puedes usar la umbralización (cv2.threshold) para crear una imagen binaria donde solo los píxeles más brillantes (potenciales llamaradas) queden en blanco y el resto en negro.

**Análisis de Contornos y Blobs:**

**Contornos:** Con cv2.findContours, puedes identificar y aislar las formas de esas regiones brillantes. A partir de los contornos, puedes calcular propiedades como el área, la posición (centroide) y la intensidad máxima dentro de esa área.

**Detección de Blobs:** La función cv2.SimpleBlobDetector es excelente para encontrar "manchas" o "gotas" en una imagen, lo cual se ajusta muy bien a la forma de una llamarada.

## **2. Clasificación de la Llamarada** 
Una vez que has identificado una región como una posible llamarada y extraído sus características (área, intensidad, etc.) con OpenCV, necesitas clasificar su magnitud.

**Extracción de Features:** Las características que calculaste en el paso anterior (área, intensidad media/máxima, forma) son las "features" o descriptores de tu llamarada.

**Entrenamiento del Modelo:** Aunque OpenCV tiene su propio módulo de Machine Learning (cv2.ml), es más común exportar estas características a una librería especializada como Scikit-learn, TensorFlow o PyTorch. Alimentarías un modelo de clasificación (como una Máquina de Soporte Vectorial, un Random Forest o una red neuronal) con las features de miles de imágenes y sus etiquetas de clase correspondientes (obtenidas de los datos de flujo de rayos X) para que aprenda a asociarlas.

En resumen, OpenCV extrae los datos visuales, y otra librería de Machine Learning los usa para aprender a clasificar.

---

## **3. Predicción de Futuras Llamaradas.** 
Esta es la parte más compleja y va más allá del análisis de una sola imagen. La predicción requiere analizar secuencias de imágenes para detectar cambios sutiles que preceden a una llamarada.

Seguimiento de Regiones Activas: Usarías OpenCV para identificar y seguir regiones activas (como grupos de manchas solares) a lo largo de varias imágenes consecutivas.

Análisis Temporal: Para cada región activa, extraerías sus características (tamaño, complejidad, intensidad) en cada imagen de la secuencia. Esto te daría una serie de tiempo de cómo evoluciona la región.

Modelo de Predicción: El modelo final no sería de visión por computadora tradicional, sino uno que entienda secuencias, como una Red Neuronal Recurrente (RNN) o un LSTM, construido con TensorFlow o PyTorch. Este modelo recibiría las series de tiempo de las características extraídas por OpenCV para predecir si una llamarada es inminente

<img width="777" height="263" alt="image" src="https://github.com/user-attachments/assets/008da8c0-19e0-4449-ad5f-cf94bd898864" />

---
## 1. Identificación de Llamaradas (Detección)
El objetivo es encontrar las zonas de la imagen que corresponden a una llamarada, que son esencialmente regiones con un brillo anómalo y repentino.

Carga y preprocesamiento: Cargar las imágenes del Sol. Como las llamaradas son fenómenos muy brillantes, un buen primer paso es convertir la imagen a escala de grises y aplicar filtros para reducir el ruido, como un filtro Gaussiano (cv2.GaussianBlur).

Detección de zonas brillantes (Thresholding): Puedes usar la umbralización (cv2.threshold) para crear una imagen binaria donde solo los píxeles más brillantes (potenciales llamaradas) queden en blanco y el resto en negro.

Análisis de Contornos y Blobs:

Contornos: Con cv2.findContours, puedes identificar y aislar las formas de esas regiones brillantes. A partir de los contornos, puedes calcular propiedades como el área, la posición (centroide) y la intensidad máxima dentro de esa área.

Detección de Blobs: La función cv2.SimpleBlobDetector es excelente para encontrar "manchas" o "gotas" en una imagen, lo cual se ajusta muy bien a la forma de una llamarada.


## 1. Abrir imagen con Spyder (Código ejemplo).
Abriremos una imagen desde Spyder.  
Script: [Abrir imagen con spyder](https://github.com/Additrejo/HackICN/blob/main/HackICN/Spyder/abrir_imagen.py)

<img width="777" height="814" alt="image" src="https://github.com/user-attachments/assets/6f085609-8139-4f5f-a2ec-7ede5e21579f" />


## 2. Identificar región luminosa.
Nuestro primer objetivo es crear un script que cargue una imagen del Sol y encuentre la región más brillante, que es el indicador más obvio de una llamarada. Usaremos una función clave de OpenCV para esto: cv2.minMaxLoc().

Paso : Encontrar el Píxel más Brillante
Este código identificará el punto exacto de mayor intensidad en la imagen y dibujará un círculo sobre él para que podamos visualizarlo.  

Script: [Región luminosa](https://github.com/Additrejo/HackICN/blob/main/HackICN/Spyder/Region_luminosa.py))  
<img width="773" height="806" alt="image" src="https://github.com/user-attachments/assets/7fdb9613-8776-47f9-84c2-ceb040de9207" />


## 3. Umbralización para Aislar la Llamarada (Thresholding).
Crea una nueva imagen donde todo lo que supere un cierto nivel de brillo se pinte de blanco, y todo lo demás se pinte de negro". El resultado es una "máscara" en blanco y negro que nos muestra exactamente la forma de la llamarada.

Script: [Umbral Thresholding](https://github.com/Additrejo/HackICN/blob/main/HackICN/Spyder/Umbral_Thresholding.py)  
<img width="796" height="816" alt="image" src="https://github.com/user-attachments/assets/7b687541-6f26-4111-add3-189c16bb3872" />


### ¿Cómo funciona?
Umbralización (cv2.threshold): Esta es la nueva línea clave. Toma la imagen en escala de grises y la convierte en una imagen binaria (la mascara).

Encontrar Contornos (cv2.findContours): Analiza la máscara en blanco y negro y devuelve una lista con las coordenadas de los perímetros de todas las formas blancas que encontró.

Dibujar Contornos (cv2.drawContours): Recorre esa lista de contornos y los dibuja sobre nuestra imagen de salida, dándonos una bonita visualización de la llamarada detectada.

###  El Parámetro Clave: El Valor del Umbral.
En el código, usamos el valor 200 en la línea cv2.threshold(gray, 200, 255, ...).

Este número es el umbral de brillo. Es el parámetro más importante que deberás ajustar.
Si aumentas este número (ej. 220), serás más estricto y solo detectarás las áreas extremadamente brillantes.
Si disminuyes este número (ej. 180), serás más permisivo y detectarás áreas más grandes o menos intensas.
Te recomiendo experimentar cambiando este valor para ver cómo afecta la detección en diferentes imágenes.

## Paso 4: Análisis de Contornos y Filtrado por Área.
La idea es simple: vamos a medir el área (el número de píxeles) de cada contorno que encontramos. Si un contorno es muy pequeño, lo ignoraremos. Si supera un tamaño mínimo, lo marcaremos como una detección válida.  

Script: [Contornos y Filtrado por Área](https://github.com/Additrejo/HackICN/blob/main/HackICN/Spyder/Filtro_por_area.py)  
<img width="519" height="804" alt="image" src="https://github.com/user-attachments/assets/b53b2ce0-f571-481e-ba83-d1afafdedd93" />

Para esto, usaremos la función cv2.contourArea().

### ¿Cuáles son los cambios clave?
Un bucle for c in contornos:: Ahora, en lugar de dibujar todos los contornos a la vez, recorremos la lista para analizar cada uno de forma individual.

Cálculo del Área (cv2.contourArea): Dentro del bucle, usamos esta función para obtener el tamaño en píxeles del contorno c que estamos analizando.

Un filtro if area > area_minima:: Esta es nuestra "puerta de control" 🗑️. Solo si el área del contorno supera el valor que definimos en area_minima, procedemos a dibujarlo. Esto limpia nuestra imagen final, mostrando únicamente las detecciones relevantes.

## Paso 5: Calcular el Centroide de la Llamarada

El centroide es, en términos simples, el centro geométrico o el "centro de masa" de una forma. Para calcularlo, OpenCV nos proporciona una herramienta matemática llamada Momentos de Imagen (cv2.moments()). A partir de estos momentos, podemos derivar fácilmente las coordenadas (x, y) del centro de la llamarada.
Esto nos da una ubicación específica para cada evento, un dato crucial para el reto.

Las nuevas líneas calculan el centroide y lo dibujan en la imagen de salida como un pequeño círculo azul.  

Script: [Calcular el Centroide de la Llamarada](https://github.com/Additrejo/HackICN/blob/main/HackICN/Spyder/Centroide.py)  
<img width="368" height="808" alt="image" src="https://github.com/user-attachments/assets/dd5e6335-5a23-4ce5-ae77-ca8dbe99dd34" />


Para cada llamarada detectada, ahora tienes:

Su tamaño: el area.

Su ubicación precisa: el centroide (cX, cY).

Esta es exactamente la clase de información que se necesita para las etapas más avanzadas del reto, como alimentar un modelo de machine learning para clasificar o predecir estos eventos.

valores, (661, 301), son las coordenadas en píxeles que marcan el centroide (el centro geométrico exacto) de la llamarada que tu programa detectó en la imagen.

Básicamente, has localizado la llamarada en el "mapa" de la imagen con una dirección precisa.

Este par de números es uno de los resultados más valiosos que hemos extraído hasta ahora.

Localización Precisa: Te permite registrar exactamente en qué parte del disco solar ocurrió el evento.

Base para el Seguimiento: Si analizaras una secuencia de imágenes (un video), podrías usar estas coordenadas para seguir el movimiento y la evolución de la llamarada a lo largo del tiempo.

Dato para Machine Learning: Has convertido un evento visual en datos numéricos estructurados (área, posición (x, y)). Este es el tipo de información que se utiliza para entrenar modelos de machine learning que pueden clasificar la intensidad de la llamarada o predecir futuras erupciones.

---

- ## Obentención de imagenes de un video.
1. Para extraer los fotogramas de un video es necesario descargar el video (preferentemente en formato .mp4).  
<img width="1134" height="559" alt="image" src="https://github.com/user-attachments/assets/afe57d69-99af-4597-9215-fb94a3a275ba" />
2. Guardarlo en una carpeta especifica.  

3. Ejecutar el siguente script: [Extracción de imagenes](código)
Modificar las siguientes lineas por la ruta del video guardado en tu carpeta.

```python
# 1. Escribe la ruta donde guardaste tu video
ruta_video = r"C:\Users\addi_\Downloads\HackICN\Solarflare\SFVideo\SFVideo.mp4"

# 2. Escribe la ruta de la carpeta donde quieres guardar las imágenes
carpeta_salida = r"C:\Users\addi_\Downloads\HackICN\Solarflare\SFVideo"

```
Al ejecutarse el script obtendremos los fotogramas.
<img width="744" height="481" alt="image" src="https://github.com/user-attachments/assets/10837e34-c9de-4dd7-bf46-ded65008c6f8" />

Tenemos todo listo para pasar al siguiente paso:

---

## Paso 5: Automatización y Procesamiento en Lote. (PENDIENTE)

Reestructurar el código para que apunte a una carpeta, analice todas las imágenes que encuentre dentro y guarde los resultados en una lista. Para esto, usaremos la librería **os** de Python, que nos permite interactuar con los archivos y carpetas del sistema.
El nuevo script hace lo siguiente:

Encapsular la lógica: Moveremos todo el código de análisis a una función reutilizable llamada analizar_imagen().

Recorrer la carpeta: El script principal definirá la ruta a una carpeta, leerá cada archivo y llamará a la función de análisis.

Recopilar los datos: Guardaremos todos los resultados (nombre del archivo, área y centroide de cada llamarada) para tener un resumen final.




