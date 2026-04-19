import numpy as np

def r(x, y, x_0, y_0):
    return np.sqrt((x - x_0)**2 + (y - y_0)**2)

def u(V, S, D, r):
    return V * r + S * (np.exp(D * r) - 1)

def b(a_0, E, y_0, x_0, x, y):
    atan = np.arctan2((y - y_0), (x - x_0))
    return a_0 - E + atan

def a(E, e, b, u):
    atan = np.arctan2(np.sin(b) * np.sin(u), np.cos(b) * np.sin(u) * np.cos(e) + np.cos(u) * np.sin(e))
    azimuth = E + atan
    # Asegurar que el azimuth esté en el rango [0, 2π]
    azimuth = np.mod(azimuth, 2 * np.pi)  # Convertir a [0, 2π]
    return azimuth

def z(e, b, u):
    in_acos = np.cos(u) * np.cos(e) - np.cos(b) * np.sin(u) * np.sin(e)
    return np.arccos(in_acos)

def position_az(a_0, x_0, y_0, x_z, y_z, e, V, S, D, posxy):
    r_t = r(posxy[0], posxy[1], x_0, y_0)
    r_z = r(x_0, y_0, x_z, y_z)
    E = a_0 + np.arctan2((y_0 - y_z), (x_0 - x_z))
    epsilon = V * r_z + S * (np.exp(D * r_z) - 1)
    b_t = b(a_0, E, y_0, x_0, posxy[0], posxy[1])
    u_t = u(V, S, D, r_t)
    azimuth = a(E, e, b_t, u_t)
    zenith = z(e, b_t, u_t)
    return (azimuth, zenith)

def horizontal_to_equatorial(azimuth, zenith, lat, lon, lst):
    """
    Convierte coordenadas horizontales (azimuth, elevación) a coordenadas ecuatoriales (RA, Dec).
    
    Parámetros:
        azimuth (float): Azimuth en grados.
        zenith (float): Elevación en grados.
        lat (float): Latitud del observador en grados.
        lon (float): Longitud del observador en grados.
        lst (float): Tiempo sidéreo local en horas.
    
    Retorna:
        ra (float): Ascensión recta en horas.
        dec (float): Declinación en grados.
    """
    # Convertir grados a radianes
    azimuth_rad = np.radians(azimuth)
    elevation = 90-zenith
    elevation_rad = np.radians(elevation)
    lat_rad = np.radians(lat)
    
    # Calcular declinación (Dec)
    sin_dec = np.sin(lat_rad) * np.sin(elevation_rad) + np.cos(lat_rad) * np.cos(elevation_rad) * np.cos(azimuth_rad)
    dec_rad = np.arcsin(sin_dec)
    dec = np.degrees(dec_rad)  # Convertir a grados
    
    # Calcular ángulo horario (H)
    cos_H = (np.sin(elevation_rad) - np.sin(lat_rad) * np.sin(dec_rad)) / (np.cos(lat_rad) * np.cos(dec_rad))
    H_rad = np.arccos(cos_H)
    H = np.degrees(H_rad)  # Convertir a grados
    
    # Ajustar el ángulo horario según el cuadrante del azimuth
    if azimuth > 180:
        H = 360 - H
    
    # Convertir ángulo horario a horas
    H_hours = H / 15  # 1 hora = 15 grados
    
    # Calcular ascensión recta (RA)
    ra = lst - H_hours
    ra = ra % 24  # Asegurar que RA esté en el rango [0, 24]
    ra = ra*(360/24)

    return ra, dec