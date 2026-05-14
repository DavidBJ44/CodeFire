import math
import json
import bui
import ffmc

"""
-generar diccinario fuego:Coge los datos iniciales y con cada tipo de suelo se crea un nuevo diccionario con la e_a y p_q asociada a cada tipo de suelo. 
-gen e p m: Con ese diccionario se crea una un doc con la matriz de suelo, la matriz de altitudes, la matriz de e_a y la p_q
!!!! falta meter la funcion bui i ffmc para q funcione auromatico
"""

def generar_diccionario_fuego(ffmc, bui, t_ambiente,m):
    # --- CONSTANTES FÍSICAS ---
    CP_MADERA = 1.4#kJ/(kg·ºC)  
    CP_AGUA = 4.18 #kJ/(kg·ºC)  
    L_VAPORIZACION = 2260 #kJ/kg
    T_IGNICION = 300    
     
  

    # --- TABLA BASE ACTUALIZADA ---
    # Estructura: 'ID': [carga_1h, carga_10h, carga_100h, K]
    # Los valores de carga están en kg/m2
    # K es una constante de transmisividad/quemado (ejemplo: entre 0.01 y 0.05)
    tabla_base = {
    '0':  [0.00, 0.00, 0.00, 0.00], #terreno urbano 
    '91': [0.0, 0.0, 0.0, 0.04], # Urbano
    '92': [0.0, 0.0, 0.0, 0.04], # Roca
    '93': [0.0, 0.0, 0.0, 0.04], # Agua
    '94': [0.0, 0.0, 0.0, 0.04], # Humedales
    '95': [0.0, 0.0, 0.0, 0.04], # Agua profunda
    '96': [0.0, 0.0, 0.0, 0.04], # Nieve
    '97': [0.0, 0.0, 0.0, 0.04], # Otros
    '98': [0.0, 0.0, 0.0, 0.04], # Quemado
    '99': [0.0, 0.0, 0.0, 0.04], # Genérico NB
    # MODELOS TIPO PASTIZAL (GR)
    '101': [0.10, 0.00, 0.00, 0.04], # GR1
    '102': [0.10, 0.00, 0.00, 0.04], # GR2
    '103': [0.10, 0.40, 0.00, 0.04], # GR3
    '104': [0.25, 0.00, 0.00, 0.04], # GR4
    '105': [0.40, 0.00, 0.00, 0.04], # GR5
    '106': [0.10, 0.00, 0.00, 0.04], # GR6
    '107': [1.00, 0.00, 0.00, 0.04], # GR7
    '108': [0.50, 1.00, 0.00, 0.04], # GR8
    '109': [1.00, 1.00, 0.00, 0.04], # GR9

    # MODELOS TIPO PASTIZAL-MATORRAL (GS)
    '121': [0.20, 0.00, 0.00, 0.04], # GS1
    '122': [0.50, 0.50, 0.00, 0.04], # GS2
    '123': [0.30, 0.25, 0.00, 0.04], # GS3
    '124': [1.90, 0.30, 0.10, 0.04], # GS4

    # MODELOS TIPO MATORRAL (SH)
    '141': [0.25, 0.25, 0.00, 0.04], # SH1
    '142': [1.35, 2.40, 0.75, 0.04], # SH2
    '143': [0.45, 3.00, 0.00, 0.04], # SH3
    '144': [0.85, 1.15, 0.20, 0.04], # SH4
    '145': [3.60, 2.10, 0.00, 0.04], # SH5
    '146': [2.90, 1.45, 0.00, 0.04], # SH6
    '147': [3.50, 5.30, 2.20, 0.04], # SH7
    '148': [2.05, 3.40, 0.85, 0.04], # SH8
    '149': [4.50, 2.45, 0.00, 0.04], # SH9

    # MODELOS TIPO MADERA-SOTOBOSQUE (TU)
    '161': [0.20, 0.90, 1.50, 0.04], # TU1
    '162': [0.95, 1.80, 1.25, 0.04], # TU2
    '163': [1.10, 0.15, 0.25, 0.04], # TU3
    '164': [4.50, 0.00, 0.00, 0.04], # TU4
    '165': [4.00, 4.00, 3.00, 0.04], # TU5

    # MODELOS TIPO HOJARASCA-SOTOBOSQUE (TL)
    '181': [1.00, 2.20, 3.60, 0.04], # TL1
    '182': [1.40, 2.30, 2.20, 0.04], # TL2
    '183': [0.50, 2.20, 2.80, 0.04], # TL3
    '184': [0.50, 1.50, 4.20, 0.04], # TL4
    '185': [1.15, 2.50, 4.40, 0.04], # TL5
    '186': [2.40, 1.20, 1.20, 0.04], # TL6
    '187': [0.30, 1.40, 8.10, 0.04], # TL7
    '188': [5.80, 1.40, 1.10, 0.04], # TL8
    '189': [6.65, 3.30, 4.15, 0.04], # TL9

    # MODELOS TIPO MADERA DERRIBADA (SB)
    '201': [1.50, 3.00, 11.00, 0.04], # SB1
    '202': [4.50, 4.25, 4.00, 0.04], # SB2
    '203': [5.50, 2.75, 3.00, 0.04], # SB3
    '204': [5.25, 3.50, 5.25, 0.04], # SB4

}

    tipos_combustible = {}

    for clave, valores in tabla_base.items():
        # Asignación de variables de la tabla
        w1h   = valores[0]
        w10h  = valores[1]
        w100h = valores[2]
        k     = valores[3]

        # --- 1. CÁLCULO ENERGÍA DE ACTIVACIÓN (E_act) ---
        term_madera = CP_MADERA * (T_IGNICION - t_ambiente)
        term_agua = m * (CP_AGUA * (100 - t_ambiente) + L_VAPORIZACION)
        q_ignicion = w1h * (term_madera + term_agua)
        
        e_act = q_ignicion * (101 - ffmc)* 400 #por metres cuadrats

        # --- 2. CÁLCULO POTENCIAL DE QUEMADO (P_Q) ---
        # Fórmula: (Suma de cargas) * (1 - e^(-K * BUI))
        carga_total = w1h + w10h + w100h
        # math.exp(x) es e^x
        factor_pq = (1 - math.exp(-k * bui)) * 18000 * 400
        p_q1 = w1h * factor_pq
        p_q2 = w10h * factor_pq
        p_q3 = w100h * factor_pq
        # --- 3. GUARDAR RESULTADOS ---
        tipos_combustible[clave] = [e_act,p_q1,p_q2,p_q3]

    return tipos_combustible

#eejmplo de uso
# --- PARÁMETROS DE ENTRADA ---
#FFMC_VALOR = 85   # humedad de combustibles finos
#BUI_VALOR = 60    # Build Up Index (Acumulación de combustible seco)
#TEMP_AMB = 35     # Temperatura ambiente
#m = 0.8           #humedad q suponemos constante en todo el terreno
## Generar el diccionario
#self_tipos_combustible = generar_diccionario_fuego(FFMC_VALOR, BUI_VALOR, TEMP_AMB,m)

## Mostrar resultado
#print(self_tipos_combustible)

import sys

def Gen_e_q_m(archivo_entrada, archivo_salida, diccionario_referencia):
    try:
        with open(archivo_entrada, 'r') as f:
            contenido = f.read().strip().split('\n\n')
            
        if len(contenido) < 2:
            print("Error: El archivo de entrada debe contener al menos dos matrices (suelo y altitud).")
            return

        # Procesar matriz de suelos
        lineas_suelo = contenido[0].strip().split('\n')
        matriz_suelos = [linea.split() for linea in lineas_suelo]
        
        # Guardar matriz de altitudes original
        matriz_altitudes_texto = contenido[1].strip()

        filas = len(matriz_suelos)
        columnas = len(matriz_suelos[0])

        # Crear listas para las nuevas matrices
        matriz_ea = []
        matriz_pq1 = []
        matriz_pq2 = []
        matriz_pq3 = []
        matriz_dieces = []

        # Mapeo de datos
        for i in range(filas):
            fila_ea, fila_pq1, fila_pq2, fila_pq3, fila_diez = [], [], [], [], []
            for j in range(columnas):
                suelo_id = matriz_suelos[i][j]
                
                if suelo_id in diccionario_referencia:
                    valores = diccionario_referencia[suelo_id]
                    # Formato esperado: [e_a, pq1, pq2, pq3]
                    fila_ea.append(str(valores[0]))
                    fila_pq1.append(str(valores[1]))
                    fila_pq2.append(str(valores[2]))
                    fila_pq3.append(str(valores[3]))
                    fila_diez.append("10") # Matriz de dieces
                else:
                    print(f"\nERROR: Suelo '{suelo_id}' en ({i},{j}) no está en el diccionario.")
                    return 
            
            matriz_ea.append(fila_ea)
            matriz_pq1.append(fila_pq1)
            matriz_pq2.append(fila_pq2)
            matriz_pq3.append(fila_pq3)
            matriz_dieces.append(fila_diez)

        # Escribir todas las matrices en el archivo de salida
        with open(archivo_salida, 'w') as f_out:
            # 1. Suelos
            f_out.write("\n".join([" ".join(f) for f in matriz_suelos]) + "\n\n")
            # 2. Altitudes
            f_out.write(matriz_altitudes_texto + "\n\n")
            # 3. E_a
            f_out.write("\n".join([" ".join(f) for f in matriz_ea]) + "\n\n")
            # 4. P_q1
            f_out.write("\n".join([" ".join(f) for f in matriz_pq1]) + "\n\n")
            # 5. P_q2
            f_out.write("\n".join([" ".join(f) for f in matriz_pq2]) + "\n\n")
            # 6. P_q3
            f_out.write("\n".join([" ".join(f) for f in matriz_pq3]) + "\n\n")
            # 7. Matriz de Dieces
            f_out.write("\n".join([" ".join(f) for f in matriz_dieces]))

        print(f"Proceso completado. Archivo '{archivo_salida}' generado con 7 matrices.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# --- EJEMPLO DE EJECUCIÓN ---
#dicc = generar_diccionario_fuego(85, 60, 35, 0.8)
#Gen_e_q_m('test_2Matrices.txt', 'salida.txt', dicc)