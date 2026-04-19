import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from transformation import *
from transformation import horizontal_to_equatorial

# Parámetros ajustados (usando los valores que proporcionaste)
import fit
a_0_fit = fit.a_0_fit
x_0_fit = fit.x_0_fit
y_0_fit = fit.y_0_fit
x_z_fit = fit.x_z_fit
y_z_fit = fit.y_z_fit
e_fit   = fit.e_fit  
V_fit   = fit.V_fit  
S_fit   = fit.S_fit  
D_fit   = fit.D_fit  

# Tamaño de la imagen
image_width = 1304
image_height = 976

# Cargar la imagen FITS
fits_file = "tu_imagen.fit"  # Reemplaza con la ruta a tu archivo FITS
with fits.open(fits_file) as hdul:
    fits_data = hdul[0].data  # Suponiendo que los datos están en la primera extensión

# Crear una malla de coordenadas (x, y)
x = np.linspace(0, image_width - 1, image_width)
y = np.linspace(0, image_height - 1, image_height)
X, Y = np.meshgrid(x, y)

# Calcular azimuth y zenith para toda la imagen
Azimuth = np.zeros_like(X)
Zenith = np.zeros_like(Y)
for i in range(image_height):
    for j in range(image_width):
        az, zen = position_az(a_0_fit, x_0_fit, y_0_fit, x_z_fit, y_z_fit, e_fit, V_fit, S_fit, D_fit, (X[i, j], Y[i, j]))
        Azimuth[i, j] = az
        Zenith[i, j] = zen
Azimuth_deg = np.rad2deg(Azimuth)
Zenith_deg = np.rad2deg(Zenith)

# Gráfico 1: Mapa de azimuth superpuesto sobre la imagen FITS
plt.figure(figsize=(10, 8))
plt.imshow(fits_data, cmap='gray', origin='lower', extent=(0, image_width, 0, image_height))  # Mostrar la imagen FITS
plt.imshow(Azimuth_deg, extent=(0, image_width, 0, image_height), origin='lower', cmap='viridis', alpha=0.3)  # Superponer el mapa de azimuth
plt.colorbar(label='Azimuth (deg)')
plt.title('Mapa de Azimuth superpuesto sobre la imagen FITS')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.savefig('azimuth.png')
plt.show()

# Gráfico 2: Mapa de zenith superpuesto sobre la imagen FITS
plt.figure(figsize=(10, 8))
plt.imshow(fits_data, cmap='gray', origin='lower', extent=(0, image_width, 0, image_height))  # Mostrar la imagen FITS
plt.imshow(Zenith_deg, extent=(0, image_width, 0, image_height), origin='lower', cmap='plasma', alpha=0.3)  # Superponer el mapa de zenith
plt.colorbar(label='Zenith (deg)')
plt.title('Mapa de Zenith superpuesto sobre la imagen FITS')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.savefig('zenith.png')
plt.show()

# transformar a ra dec
latitude = -33.3961  
longidute = -70.537
lst = 6.3193001276

RA = np.zeros_like(Azimuth)
DEC = np.zeros_like(Zenith)
for i in range(image_height):
    for j in range(image_width):
        ra, dec = horizontal_to_equatorial(Azimuth_deg[i,j], Zenith_deg[i,j], latitude, longidute, lst)
        RA[i, j] = ra
        DEC[i, j] = dec


plt.figure(figsize=(10, 8))
plt.imshow(fits_data, cmap='gray', origin='lower', extent=(0, image_width, 0, image_height))  # Mostrar la imagen FITS
plt.imshow(RA, extent=(0, image_width, 0, image_height), origin='lower', cmap='plasma', alpha=0.3)  # Superponer el mapa de zenith
plt.colorbar(label='RA (hour)')
plt.title('Mapa de RA superpuesto sobre la imagen FITS')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.savefig('rightasension.png')
plt.show()

plt.figure(figsize=(10, 8))
plt.imshow(fits_data, cmap='gray', origin='lower', extent=(0, image_width, 0, image_height))  # Mostrar la imagen FITS
plt.imshow(DEC, extent=(0, image_width, 0, image_height), origin='lower', cmap='plasma', alpha=0.3)  # Superponer el mapa de zenith
plt.colorbar(label='DEC (deg)')
plt.title('Mapa de DEC superpuesto sobre la imagen FITS')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.savefig('declination.png')
plt.show()

"""
# Cargar la imagen FITS
fits_file = "tu_imagen.fit"  # Reemplaza con la ruta a tu archivo FITS
with fits.open(fits_file) as hdul:
    fits_data = hdul[0].data  # Suponiendo que los datos están en la primera extensión
    header = hdul[0].header   # Obtener el encabezado FITS

# Crear una proyección Aitoff
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection="aitoff")

# Graficar la imagen FITS en la proyección Aitoff
# Nota: Necesitamos convertir las coordenadas (RA, DEC) a radianes y ajustar el rango de RA
RA_rad = np.radians(RA)  # Convertir RA a radianes
DEC_rad = np.radians(DEC)  # Convertir DEC a radianes

# Ajustar el rango de RA para que esté en [-180, 180] grados
RA_rad[RA_rad > np.pi] -= 2 * np.pi

# Graficar la imagen usando scatter (puede ser lento para imágenes grandes)
# Aquí usamos un submuestreo para mejorar el rendimiento
step = 1  # Submuestreo para reducir el número de puntos
ax.scatter(RA_rad[::step, ::step], DEC_rad[::step, ::step], c=fits_data[::step, ::step], 
           cmap='gray', s=1, alpha=1)

# Añadir etiquetas y título
ax.set_xlabel('RA (rad)')
ax.set_ylabel('Dec (rad)')
ax.set_title('Imagen FITS en proyección Aitoff')
ax.grid(True)
plt.savefig('aitoff.jpg')
# Mostrar el gráfico
plt.show()
"""

import numpy as np
import matplotlib.pyplot as plt

# Función para calcular la distancia angular entre dos puntos (RA, DEC) en grados
def angular_distance(ra1, dec1, ra2, dec2):
    """
    Calcula la distancia angular entre dos puntos (RA, DEC) en grados.
    Usa la fórmula del haversine.
    """
    ra1_rad = np.radians(ra1)
    dec1_rad = np.radians(dec1)
    ra2_rad = np.radians(ra2)
    dec2_rad = np.radians(dec2)
    
    # Fórmula del haversine
    d_ra = ra2_rad - ra1_rad
    d_dec = dec2_rad - dec1_rad
    a = np.sin(d_dec / 2)**2 + np.cos(dec1_rad) * np.cos(dec2_rad) * np.sin(d_ra / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(c)  # Convertir a grados

# Calcular el mapa de la escala de píxeles
def calculate_pixel_scale(RA, DEC):
    """
    Calcula la escala de píxeles (en grados por píxel) para cada píxel de la imagen.
    """
    image_height, image_width = RA.shape
    pixel_scale = np.zeros_like(RA)
    
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            # Calcular la distancia angular con los vecinos
            dist_x = angular_distance(RA[i, j], DEC[i, j], RA[i, j + 1], DEC[i, j + 1])
            dist_y = angular_distance(RA[i, j], DEC[i, j], RA[i + 1, j], DEC[i + 1, j])
            
            # Promediar las distancias para obtener la escala de píxeles
            pixel_scale[i, j] = (dist_x + dist_y) / 2
    
    return pixel_scale

# Calcular el mapa de la escala de píxeles
pixel_scale_map = calculate_pixel_scale(RA, DEC)

# Graficar el mapa de la escala de píxeles
plt.figure(figsize=(10, 8))
plt.imshow(pixel_scale_map[1:-1, 1:-1], origin='lower', cmap='viridis', extent=(0, image_width, 0, image_height))
plt.colorbar(label='Escala de píxeles (grados por píxel)')
plt.title('Mapa de la escala de píxeles')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.savefig('pixelscale.png')
plt.show()