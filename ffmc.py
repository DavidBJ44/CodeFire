import math
import numpy as np
import pandas as pd

def RainCode(ffmc_actual, lluvia):
    try:
        pd.read_csv('csv/table1.csv', index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError("table1.csv no encontrado en el directorio actual.")
    
    valores_r = table.columns.astype(float)
    valores_ffmc = table.index.astype(float)
    
    idx_ffmc = np.searchsorted(valores_ffmc, ffmc_actual, side='right') - 1
    idx_ffmc = max(0, idx_ffmc)
    
    idx_lluvia = np.searchsorted(valores_r, lluvia, side='right') - 1
    idx_lluvia = max(0, idx_lluvia)
    
    return table.iloc[idx_ffmc, idx_lluvia]

def calcular_ffmc(matriz):
    # Assume matriz is a 30x4 NumPy array: rows = days (0-29), columns = [temp (°C), rh (%), wind (km/h), rain (mm)]
    if matriz.shape != (30, 4):
        raise ValueError("La matriz de fmmc debe tener 30 filas y 4 columnas.")
    
    
    ffmc = 85.0  # Initial FFMC value
    
    for dia in range(0, 29):  # Loop from day 1 to 29
        T = matriz[dia, 0]  # Temperature
        H = matriz[dia, 1]  # Relative humidity
        W = matriz[dia, 2]  # Wind speed
        R = matriz[dia, 3]  # Rainfall
        if R > 0.59:
            ffmc = RainCode(ffmc, R, matriz)
        ffmc = table2(T, H, W, ffmc)
        dia += 1
    return ffmc

def table2(temperatura, humedad, viento, ffmc_actual):
    if temperatura < 25:
        tabla = pd.read_csv('csv/table2_20-25.csv', index_col=[0, 1])
    elif temperatura < 30:
        tabla = pd.read_csv('csv/table2_25-30.csv', index_col=[0, 1])
    elif temperatura < 35:
        tabla = pd.read_csv('csv/table2_30-35.csv', index_col=[0, 1])
    else:
        raise ValueError("Temperatura fuera de rango para las tablas disponibles (debe ser < 35°C).")
    
    humedades = np.unique(tabla.index.get_level_values(0).astype(float))
    vientos = np.unique(tabla.index.get_level_values(1).astype(float))
    ffmcs = tabla.columns.astype(float)
    
    idx_humedad = np.searchsorted(humedades, humedad, side='right') - 1
    idx_humedad = max(0, idx_humedad)
    
    idx_viento = np.searchsorted(vientos, viento, side='right') - 1
    idx_viento = max(0, idx_viento)
    
    idx_ffmc = np.searchsorted(ffmcs, ffmc_actual, side='right') - 1
    idx_ffmc = max(0, idx_ffmc)
    
    humedad_seleccionada = humedades[idx_humedad]
    viento_seleccionado = vientos[idx_viento]
    
    return tabla.loc[(humedad_seleccionada, viento_seleccionado), tabla.columns[idx_ffmc]]


