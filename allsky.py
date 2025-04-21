import zwoasi as asi
import os
import time
from PIL import Image
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timedelta
import numpy as np
import threading

# Configuración de la cámara
ruta_sdk = 'C:/ASI_SDK'
#os.environ['ZWO_ASI_LIB'] = os.path.join(ruta_sdk, 'ASI_API.dll')  # Windows
os.environ['ZWO_ASI_LIB'] = os.path.join(ruta_sdk, 'libASICamera2.so')  # Linux

# Inicializar la cámara
asi.init(ruta_sdk)
num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    raise Exception('No se encontraron cámaras ZWO ASI conectadas.')
camera = asi.Camera(0)
camera_info = camera.get_camera_property()
print(f'Conectado a la cámara: {camera_info["Name"]}')

# Configuración inicial
exposicion = 1000000  # ms
ganancia = 100 
brillo_objetivo = 128


def calcular_brillo(image):
    return np.mean(image)


def ajustar_exposicion_ganancia(image):
    global exposicion, ganancia
    brillo = calcular_brillo(image)

    # Ajustar exposición
    if brillo < brillo_objetivo * 0.9:  # Subexpuesta
        exposicion = min(exposicion * 1.5, 30000000)  # Aumentar exposición (máximo 30 segundos)
    elif brillo > brillo_objetivo * 1.1:  # Sobreexpuesta
        exposicion = max(exposicion / 1.5, 1000)  # Reducir exposición (mínimo 1 ms)

    # Ajustar ganancia
    if brillo < brillo_objetivo * 0.8:  # Subexpuesta
        ganancia = min(ganancia + 10, 500)  # Aumentar ganancia (máximo 500)
    elif brillo > brillo_objetivo * 1.2:  # Sobreexpuesta
        ganancia = max(ganancia - 10, 0)  # Reducir ganancia (mínimo 0)

    # Aplicar los nuevos valores a la cámara
    camera.set_control_value(asi.ASI_EXPOSURE, int(exposicion))
    camera.set_control_value(asi.ASI_GAIN, int(ganancia))
    print(f'Ajuste: Exposición = {exposicion/1000} ms, Ganancia = {ganancia}')


def capturar_imagen():
    # Obtener la fecha y hora actual
    noche = datetime.now() - timedelta(hours=12)
    fecha = noche.strftime('%Y-%m-%d')  

    # Crear el directorio de la fecha si no existe
    directorio_fecha = os.path.join('imagenes', fecha)
    if not os.path.exists(directorio_fecha):
        os.makedirs(directorio_fecha)

    # Capturar la imagen
    print('Capturando imagen...')
    image = camera.capture()
    im = Image.fromarray(image)
    ajustar_exposicion_ganancia(image)

    # saving
    im.save('allsky.png')
    print('Imagen guardada como allsky.png')

    hora = datetime.now().strftime('%H_%M_%S')
    ruta_imagen = os.path.join(directorio_fecha, f'{hora}.png')
    im.save(ruta_imagen)
    print(f'Imagen guardada en {ruta_imagen}')

# Clase para manejar las solicitudes HTTP
class AllSkyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/allsky.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('allsky.png', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

# Crear el archivo HTML
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AllSky Camera</title>
    <style>
        /* Estilo para centrar solo la imagen */
        .imagen-centrada {
            display: block;           /* Hace que la imagen se comporte como un bloque */
            margin: 0 auto;          /* Centra horizontalmente */
            max-width: 80%;          /* Limita el ancho de la imagen al 80% */
            height: auto;            /* Mantiene la proporción de la imagen */
        }
        /* Estilo para el cuerpo de la página */
        body {
            background-color: #000;  /* Fondo negro */
            color: white;           /* Color del texto */
            text-align: center;     /* Centra el texto horizontalmente */
        }
        /* Estilo para el párrafo de la fecha */
        p {
            margin-top: 20px;       /* Espacio entre la imagen y el texto */
        }
    </style>
</head>
<body>
    <h1>AllSky Camera</h1>
    <img src="/allsky.png" alt="AllSky Image" class="imagen-centrada">
    <p>Última actualización: <span id="fecha"></span></p>
    <script>
        function actualizarFecha() {
            const fecha = new Date();
            document.getElementById('fecha').textContent = fecha.toLocaleString();
        }
        actualizarFecha();
        setInterval(actualizarFecha, 30000);  // Actualizar cada segundo
    </script>
</body>
</html>
"""
with open('index.html', 'w') as f:
    f.write(html_content)

# Iniciar el servidor web
def iniciar_servidor():
    server_address = ('', 8000)  # Servidor en localhost:8000
    httpd = HTTPServer(server_address, AllSkyHandler)
    print('Servidor web iniciado en http://localhost:8000')
    httpd.serve_forever()
threading.Thread(target=iniciar_servidor, daemon=True).start()


try:
    while True:
        ahora = datetime.now().strftime('%H')
        if int(ahora) > 19 and int(ahora) < 7:
            capturar_imagen()
            time.sleep(60)  # Esperar 1 minuto
        else:
            print('Camara en Daytime... Mostrando Ultima Foto')
except KeyboardInterrupt:
    print('Deteniendo la captura y el servidor...')
finally:
    camera.close()