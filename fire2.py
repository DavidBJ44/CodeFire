import numpy as np
# Añade esto al principio del archivo, después de los imports
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def avance_fuego(nombre_archivo_entrada, nombre_archivo_salida):
        # --- 1. LEER Y CARGAR LAS 4 MATRICES ---
    try:
        with open(nombre_archivo_entrada, 'r') as f:
            bloques = f.read().strip().split('\n\n')
        
        if len(bloques) < 7:
            print("Error: El archivo de entrada debe tener 4 matrices (Suelo, Altitud, Ea, Pq).")
            return

        # Cargamos las matrices
        # Matriz 0: Suelos (String para poder usar 'f' y '1')
        A_terreno = np.array([linea.split() for linea in bloques[0].split('\n')], dtype=str)
        # Matriz 1: Altitud (Float)
        A_altitud = np.array([linea.split() for linea in bloques[1].split('\n')], dtype=float)
        # Matriz 2: Resistencias/Ea (Float)
        A_resistencias = np.array([linea.split() for linea in bloques[2].split('\n')], dtype=float)
        # Matriz 3-6: Potencial/Pq (Float)
        A_pq1 = np.array([linea.split() for linea in bloques[3].split('\n')], dtype=float)
        A_pq2 = np.array([linea.split() for linea in bloques[4].split('\n')], dtype=float)
        A_pq3 = np.array([linea.split() for linea in bloques[5].split('\n')], dtype=float)
        
        # Matriz 7 de contadores (la de los dieces)
        A_contador = np.array([linea.split() for linea in bloques[6].split('\n')], dtype=float)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    tabla_beta = {
    # Estructura: 'ID': [beta, sigma]
    '0':  [None, None], #terreno urbano 
    '91': [None, None], # Urbano
    '92': [None, None], # Roca
    '93': [None, None], # Agua
    '94': [None, None], # Humedales
    '95': [None, None], # Agua profunda
    '96': [None, None], # Nieve
    '97': [None, None], # Otros
    '98': [None, None], # Quemado
    '99': [None, None], # Genérico NB
    # MODELOS TIPO PASTIZAL (GR)
    '101': [0.00143, 2054], # GR1
    '102': [0.00158, 1820], # GR2
    '103': [0.00143, 1290], # GR3
    '104': [0.00154, 1826], # GR4
    '105': [0.00277, 1631], # GR5
    '106': [0.00335, 2006], # GR6
    '107': [0.00306, 1834], # GR7
    '108': [0.00316, 1302], # GR8
    '109': [0.00316, 1612], # GR9

    # MODELOS TIPO PASTIZAL-MATORRAL (GS)
    '121': [0.00215, 1832], # GS1
    '122': [0.00249, 1827], # GS2
    '123': [0.00259, 1614], # GS3
    '124': [0.00874, 1674], # GS4

    # MODELOS TIPO MATORRAL (SH)
    '141': [0.00280, 1674], # SH1
    '142': [0.01198, 1672], # SH2
    '143': [0.00577, 1371], # SH3
    '144': [0.00227, 1682], # SH4
    '145': [0.00206, 1252], # SH5
    '146': [0.00412, 1144], # SH6
    '147': [0.00344, 1233], # SH7
    '148': [0.00509, 1386], # SH8
    '149': [0.00505, 1378], # SH9

    # MODELOS TIPO MADERA-SOTOBOSQUE (TU)
    '161': [0.00885, 1606], # TU1
    '162': [0.00603, 1767], # TU2
    '163': [0.00359, 1611], # TU3
    '164': [0.01865, 2216], # TU4
    '165': [0.02009, 1224], # TU5

    # MODELOS TIPO HOJARASCA-SOTOBOSQUE (TL)
    '181': [0.04878, 1716], # TL1
    '182': [0.04232, 1806], # TL2
    '183': [0.02630, 1532], # TL3
    '184': [0.02224, 1568], # TL4
    '185': [0.01925, 1713], # TL5
    '186': [0.02296, 1936], # TL6
    '187': [0.03515, 1229], # TL7
    '188': [0.03969, 1770], # TL8
    '189': [0.03372, 1733], # TL9

    # MODELOS TIPO MADERA DERRIBADA (SB)
    '201': [0.02224, 1653], # SB1
    '202': [0.01829, 1884], # SB2
    '203': [0.01345, 1935], # SB3
    '204': [0.00744, 1907], # SB4
    }
    n, m = A_terreno.shape
    cell_size = 20.0
    
    # Direcciones y sus distancias (para diagonales usamos la hipotenusa)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    distancias = [cell_size, cell_size, cell_size, cell_size, cell_size * np.sqrt(2), cell_size * np.sqrt(2), cell_size * np.sqrt(2), cell_size * np.sqrt(2)]
    
    
    
    x = int(input(f"¿En qué fila quieres que empiece el fuego? (0-{n-1}): "))
    y = int(input(f"¿En qué columna quieres que empiece el fuego? (0-{m-1}): "))
    
    # Validar que las coordenadas están dentro del rango
    if not (0 <= x < n and 0 <= y < m):
        print(f"Error: las coordenadas deben estar dentro de [0-{n-1}, 0-{m-1}]")
        return []
    
    # Inicializar matriz de terreno, cambiar inicial a quemando
    A_terreno[x, y] = 'f'  # Fuego inicial quemando
    
    A_terreno_list = [A_terreno.copy()]
    
   # --- BUCLE PRINCIPAL ---
    while np.any(A_terreno == 'f'):
        A_terreno_nueva = A_terreno.copy()
        quemando = np.where(A_terreno == 'f')
        coords_quemando = list(zip(quemando[0], quemando[1]))

        for i, j in coords_quemando:
            # 1. Determinar Potencial Emisor de la casilla que quema (i, j)
            c = A_contador[i, j]
            p_emisor = 0
            
            # Intervalos según tus instrucciones (con solapamientos)
            if 7 <= c <= 10:
                p_emisor += (A_pq1[i, j] / 2)
            if 4 <= c <= 8:
                p_emisor += (A_pq2[i, j] / 3)
            if 0 <= c <= 7:
                p_emisor += (A_pq3[i, j] / 7)

            # 2. Afectar a las colindantes
            for (di, dj), dist in zip(direcciones, distancias):
                ni, nj = i + di, j + dj
                
                # Celdas que pueden recibir daño
                if 0 <= ni < n and 0 <= nj < m and A_terreno[ni, nj] not in ['f', '1', '0', '91', '92', '93', '94', '95', '96', '97', '98', '99']:
                    
                    # Pendiente y Beta (del terreno destino)
                    dz = A_altitud[ni, nj] - A_altitud[i, j]
                    tan_phi = dz / dist
                    tipo_terreno_ni = A_terreno[ni, nj]
                    beta = tabla_beta.get(tipo_terreno_ni, [None])[0]

                    if tan_phi <= 0 or beta is None:
                        phi_s = 1
                    else:
                        if tan_phi >= 1:
                            phi_s = 1 + (5.275 * (beta ** (-0.3)) * (1 ** 2))
                        else:
                            phi_s = 1 + (5.275 * (beta ** (-0.3)) * (tan_phi ** 2))

                    potencial_efectivo = p_emisor * phi_s
                    
                    # Restar a la resistencia de la casilla colindante
                    A_resistencias[ni, nj] -= potencial_efectivo
                    
                    # Si se agota la energía de activación, empieza a arder
                    if A_resistencias[ni, nj] <= 0:
                        A_terreno_nueva[ni, nj] = 'f'

            # 3. Restar al contador de la casilla que está ardiendo
            A_contador[i, j] -= 1
            
            # 4. Si el contador se agota, la casilla se apaga
            if A_contador[i, j] < 0:
                A_terreno_nueva[i, j] = '98'
        
        A_terreno = A_terreno_nueva
        A_terreno_list.append(A_terreno.copy())
        
        if not np.any(A_terreno == 'f'):
            break

    # --- GUARDAR RESULTADOS ---
    def formatear_matriz(matriz):
        return "\n".join([" ".join(map(str, fila)) for fila in matriz])

    with open(nombre_archivo_salida, 'w') as f_out:
        # El primer estado
        f_out.write(formatear_matriz(A_terreno_list[0]))
        f_out.write("\n\n")
        # Los siguientes pasos de tiempo
        for paso in A_terreno_list[1:]:
            f_out.write(formatear_matriz(paso))
            f_out.write("\n\n")

    print(f"Simulación finalizada. Resultados en '{nombre_archivo_salida}'")

#avance_fuego('salida.txt', 'evolucion_fuego.txt')