import math
import json

def generar_diccionario_fuego(ffmc, bui, t_ambiente):
    # --- CONSTANTES FÍSICAS ---
    CP_MADERA = 1465      
    CP_AGUA = 4186        
    L_VAPORIZACION = 2257000 
    T_IGNICION = 320      

    # --- TABLA BASE ACTUALIZADA ---
    # Estructura: 'ID': [carga_1h, humedad_M, carga_10h, carga_100h, K]
    # Los valores de carga están en kg/m2
    # K es una constante de transmisividad/quemado (ejemplo: entre 0.01 y 0.05)
    tabla_base = {
        'T1': [0.15, 0.05, 0.10, 0.05, 0.02], 
        'T2': [0.40, 0.10, 0.30, 0.20, 0.03], 
        'T3': [0.80, 0.15, 1.50, 3.00, 0.04], 
        'T4': [0.00, 0.00, 0.00, 0.00, 0.00],
    }

    tipos_combustible = {}

    for clave, valores in tabla_base.items():
        # Asignación de variables de la tabla
        w1h   = valores[0]
        m     = valores[1]
        w10h  = valores[2]
        w100h = valores[3]
        k     = valores[4]

        # --- 1. CÁLCULO ENERGÍA DE ACTIVACIÓN (E_act) ---
        term_madera = CP_MADERA * (T_IGNICION - t_ambiente)
        term_agua = m * (CP_AGUA * (100 - t_ambiente) + L_VAPORIZACION)
        q_ignicion = w1h * (term_madera + term_agua)
        
        e_act = q_ignicion * (101 - ffmc)

        # --- 2. CÁLCULO POTENCIAL DE QUEMADO (P_Q) ---
        # Fórmula: (Suma de cargas) * (1 - e^(-K * BUI))
        carga_total = w1h + w10h + w100h
        # math.exp(x) es e^x
        p_q = carga_total * (1 - math.exp(-k * bui))

        # --- 3. GUARDAR RESULTADOS ---
        tipos_combustible[clave] = {
            'e_act': e_act,
            'p_q': p_q
        }

    return tipos_combustible

# --- PARÁMETROS DE ENTRADA ---
FFMC_VALOR = 85   # Humedad de combustibles finos
BUI_VALOR = 40    # Build Up Index (Acumulación de combustible seco)
TEMP_AMB = 25     # Temperatura ambiente

# Generar el diccionario
self_tipos_combustible = generar_diccionario_fuego(FFMC_VALOR, BUI_VALOR, TEMP_AMB)

# Mostrar resultado
print(json.dumps(self_tipos_combustible, indent=4))