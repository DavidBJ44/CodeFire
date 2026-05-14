import math
import numpy as np
import pandas as pd

def lookup_le(sorted_values, target):
    idx = np.searchsorted(sorted_values, target, side='right') - 1
    return max(0, idx)


def RainCode(ffmc_actual, lluvia):
    try:
        table = pd.read_csv('csv/table1.csv', index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError("table1.csv no encontrado en el directorio actual.")
    
    valores_r = table.columns.astype(float)
    valores_ffmc = table.index.astype(float)
    
    idx_ffmc = lookup_le(valores_ffmc, ffmc_actual)
    idx_lluvia = lookup_le(valores_r, lluvia)
    
    return table.iloc[idx_ffmc, idx_lluvia]

def calcular_ffmc(matriz):
    # Assume matriz is a 31x4 NumPy array: rows = days (0-30), columns = [temp (°C), rh (%), rain (mm), wind (km/h)]
    if matriz.shape != (31, 4):
        raise ValueError("La matriz de fmmc debe tener 31 filas y 4 columnas.")
    
    
    ffmc = 85.0  # Initial FFMC value
    
    for dia in range(31):  # Loop from day 1 to 31
        T = matriz[dia, 0]  # Temperature
        H = matriz[dia, 1]  # Relative humidity
        R = matriz[dia, 2]  # Rainfall
        W = matriz[dia, 3]  # Wind speed
        if R > 0.59:
            ffmc = RainCode(ffmc, R)
        ffmc = table2(T, H, W, ffmc)
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
    
    idx_humedad = lookup_le(humedades, humedad)
    idx_viento = lookup_le(vientos, viento)
    idx_ffmc = lookup_le(ffmcs, ffmc_actual)
    
    humedad_seleccionada = humedades[idx_humedad]
    viento_seleccionado = vientos[idx_viento]
    
    return tabla.loc[(humedad_seleccionada, viento_seleccionado), tabla.columns[idx_ffmc]]
