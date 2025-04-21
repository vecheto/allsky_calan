import time
import os
import shutil

def calcular_tamanio_carpeta(ruta_carpeta):
    """
    Calcula el tamaño total de una carpeta y sus subcarpetas en bytes.
    """
    tamanio_total = 0  # Tamaño total en bytes

    # Recorre todos los archivos y subcarpetas
    for ruta_actual, _, archivos in os.walk(ruta_carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_actual, archivo)
            tamanio_total += os.path.getsize(ruta_completa)

    return tamanio_total


def verificar_espacio_carpeta(ruta_carpeta, limite_tamanio_gb=None):
    """
    Verifica el espacio ocupado por la carpeta y muestra un mensaje.
    Si se proporciona un límite en GB, verifica si se ha excedido.
    """
    # Calcular el tamaño de la carpeta
    tamanio_bytes = calcular_tamanio_carpeta(ruta_carpeta)
    tamanio_formateado_gb = tamanio_bytes / (1024 * 1024 * 1024)

    print(f"El tamaño de la carpeta '{ruta_carpeta}' es: {tamanio_formateado_gb} GB")

    # Verificar si se ha excedido el límite de tamaño
    if limite_tamanio_gb is not None:
        limite_bytes = limite_tamanio_gb * 1024 * 1024 * 1024
        if tamanio_bytes > limite_bytes:
            print(f"¡Advertencia! La carpeta ha excedido el límite de {limite_tamanio_gb} GB.")
            return True
        else:
            print(f"La carpeta está dentro del límite de {limite_tamanio_gb} GB.")
            return False


def eliminar_directorio_antiguo(ruta_carpeta):
    """
    Elimina el directorio más antiguo si el tamaño de la carpeta excede el límite.
    """
    directorios = []
    for nombre_directorio in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, nombre_directorio)
        if os.path.isdir(ruta_completa):  # Verificar que sea un directorio
            tiempo_modificacion = os.path.getmtime(ruta_completa)
            directorios.append((ruta_completa, tiempo_modificacion))

    if not directorios:
        return None  # No hay directorios

    # Obtener el directorio más antiguo
    directorio_antiguo = min(directorios, key=lambda x: x[1])

    directorio_antiguo = directorio_antiguo[0]
    if not directorio_antiguo:
        print("No hay más directorios para eliminar.")

    # Eliminar el directorio más antiguo
    print(f"Eliminando directorio antiguo: {directorio_antiguo}")
    shutil.rmtree(directorio_antiguo)  # Elimina el directorio y su contenido


# Ruta de la carpeta "imagenes"
ruta_imagenes = os.path.join('imagenes')

try:
    while True:
        exceed = verificar_espacio_carpeta(ruta_imagenes, limite_tamanio_gb=10)
        if exceed:
            eliminar_directorio_antiguo(ruta_imagenes)
        time.sleep(60)  # Esperar 1 minuto

except KeyboardInterrupt:
    print('Deteniendo la evaluacion de espacio...')
