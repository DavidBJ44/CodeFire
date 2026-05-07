import math
import numpy as np
import pandas as pd

def calcular_bui(matriz):
    # Assume matriz is a 30x4 NumPy array: rows = days (0-29), columns = [temp (°C), rh (%), rain (mm)]
    if matriz.shape != (30, 4):
        raise ValueError("La matriz de BUI debe tener 30 filas y 3 columnas.")
    
    primera_fila = None
    for i in range(29,-1,-1):
        if matriz[i, 3] > 1.5:
            primera_fila = i
            break
    
    if primera_fila is None:
        dmc = 50.0  # Valor inicial de DMC
        dc = 350.0  # Valor inicial de DC
        for dia in range(0, 29):  # Loop from day 1 to 29
            T = matriz[dia, 0]  # Temperature
            H = matriz[dia, 1]  # Relative humidity
            R = matriz[dia, 3]  # Rainfall
            if R > 1.5:
                dmc = raincode_DMC(R, dmc)
                dc = raincode_DC(R, dc)
            dmc = table4(T,H)
            dc = table6(T)
            bui = table8(dmc, dc)
    
    else:
        for dia in range(i, 29):
            T = matriz[dia, 0]  # Temperature
            H = matriz[dia, 1]  # Relative humidity
            R = matriz[dia, 3]  # Rainfall
            if R > 1.5:
                dmc = raincode_DMC(R, dmc)
                dc = raincode_DC(R, dc)
            dmc = table4(T,H)
            dc = table6(T)
            bui = table8(dmc, dc) 
    return bui


def raincode_DMC(rain, dmc):
    try:
        table = pd.read_csv('csv/table3.csv', index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError("table3.csv no encontrado en el directorio actual.")
    valores_r = table.columns.astype(float)
    valores_dmc = table.index.astype(float)
    
    idx_dmc = np.searchsorted(valores_dmc, dmc, side='right') - 1
    idx_dmc = max(0, idx_dmc)
    
    idx_lluvia = np.searchsorted(valores_r, rain, side='right') - 1
    idx_lluvia = max(0, idx_lluvia)
    
    return table.iloc[idx_dmc, idx_lluvia]

def raincode_DC(rain, dc):
    try:
        table = pd.read_csv('csv/table5.csv', index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError("table5.csv no encontrado en el directorio actual.")
    valores_r = table.columns.astype(float)
    valores_dc = table.index.astype(float)
    
    idx_dc = np.searchsorted(valores_dc, dc, side='right') - 1
    idx_dc = max(0, idx_dc)
    
    idx_lluvia = np.searchsorted(valores_r, rain, side='right') - 1
    idx_lluvia = max(0, idx_lluvia)
    
    return table.iloc[idx_dc, idx_lluvia]

def table4(temperatura, humedad):
    """Busca en csv/table4.csv el valor según temperatura y humedad.

    Selecciona la temperatura y humedad más altas que sean menores o iguales
    """
    table = pd.read_csv('csv/table4.csv')

    temp_col = table.columns[0]
    rh_col = table.columns[1]
    value_col = table.columns[-1]

    table[temp_col] = table[temp_col].astype(float)
    table[rh_col] = table[rh_col].astype(float)

    temps = np.sort(table[temp_col].unique())
    idx_temp = np.searchsorted(temps, temperatura, side='right') - 1
    temp_key = temps[max(0, idx_temp)]

    subset = table[table[temp_col] == temp_key]
    rhs = np.sort(subset[rh_col].unique())
    idx_rh = np.searchsorted(rhs, humedad, side='right') - 1
    rh_key = rhs[max(0, idx_rh)]

    return subset[subset[rh_col] == rh_key].iloc[0][value_col]


def table6(temperatura):
    """Busca en csv/table6.csv el valor según temperatura.

    Selecciona la temperatura más alta que sea menor o igual a la solicitada.
    """
    try:
        table = pd.read_csv('csv/table6.csv')
    except FileNotFoundError:
        raise FileNotFoundError("table6.csv no encontrado en el directorio actual.")
    if table.shape[1] < 2:
        raise ValueError("table6.csv debe tener al menos dos columnas: temperatura y valor.")

    temp_col = table.columns[0]
    value_col = table.columns[1]
    table[temp_col] = table[temp_col].astype(float)

    temps = np.sort(table[temp_col].unique())
    idx_temp = np.searchsorted(temps, temperatura, side='right') - 1
    idx_temp = max(0, idx_temp)
    temp_key = temps[idx_temp]

    row = table[table[temp_col] == temp_key].iloc[0]
    return row[value_col]

def table8(dmc, dc):
    """Busca en csv/table8.csv el valor según DMC y DC.

    Selecciona el DMC y DC más altos que sean menores o iguales
    a los valores solicitados, usando np.searchsorted.
    """
    table = pd.read_csv('csv/table8.csv', index_col=0)
    valores_dc = table.columns.astype(float)
    valores_dmc = table.index.astype(float)
    
    idx_dmc = np.searchsorted(valores_dmc, dmc, side='right') - 1
    idx_dmc = max(0, idx_dmc)
    
    idx_dc = np.searchsorted(valores_dc, dc, side='right') - 1
    idx_dc = max(0, idx_dc)
    
    return table.iloc[idx_dmc, idx_dc]