import numpy as np
from scipy.optimize import curve_fit
from transformation import *
import pandas as pd

# Definir las funciones que ya tienes

# Función para el ajuste
def fit_function(posxy, a_0, x_0, y_0, x_z, y_z, e, V, S, D):
    posxy = np.reshape(posxy, (-1, 2))
    results = []
    for xy in posxy:
        r_t = r(xy[0], xy[1], x_0, y_0)
        r_z = r(x_0, y_0, x_z, y_z)
        E = a_0 + np.arctan2((y_0 - y_z), (x_0 - x_z))
        epsilon = V * r_z + S * (np.exp(D * r_z) - 1)
        b_t = b(a_0, E, y_0, x_0, xy[0], xy[1])
        u_t = u(V, S, D, r_t)
        azimuth = a(E, e, b_t, u_t)
        zenith = z(e, b_t, u_t)
        results.append(azimuth)
        results.append(zenith)
    return np.array(results)

# Datos de ejemplo
data = pd.read_csv('data.csv')
xy_data = np.array(data[['x','y']])
az_data = np.array(data[['a','z']])
xy_data_flat = xy_data.flatten()
az_data_flat = az_data.flatten()

# Valores iniciales
initial_guess = [0, 652, 488, 652, 488, 0, 0, 0, 0]  # a_0, x_0, y_0, x_z, y_z, e, V, S, D

# Límites
lower_bounds = [0, 0, 0, 0, 0, -np.pi / 2, -10, -10, -10]
upper_bounds = [2 * np.pi, 1304, 976, 1304, 976, np.pi / 2, 10, 10, 10]
bounds = (lower_bounds, upper_bounds)

# Realizar el ajuste
try:
    params, covariance = curve_fit(
                                    fit_function, 
                                    xy_data_flat, 
                                    az_data_flat, 
                                    p0=initial_guess, 
                                    bounds=bounds, 
                                    method='trf'  # Usamos 'trf' para problemas con límites
                                    )
    # Parámetros ajustados
    a_0_fit, x_0_fit, y_0_fit, x_z_fit, y_z_fit, e_fit, V_fit, S_fit, D_fit = params

    print("Parámetros ajustados:")
    print(f"a_0: {a_0_fit}")
    print(f"x_0: {x_0_fit}")
    print(f"y_0: {y_0_fit}")
    print(f"x_z: {x_z_fit}")
    print(f"y_z: {y_z_fit}")
    print(f"e__: {e_fit}")
    print(f"V__: {V_fit}")
    print(f"S__: {S_fit}")
    print(f"D__: {D_fit}")
    
except Exception as e:
    print(f"Error durante el ajuste: {e}")