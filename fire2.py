import numpy as np
# Añade esto al principio del archivo, después de los imports
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def avance_fuego(nombre_archivo_entrada, nombre_archivo_salida):
        # --- 1. LEER Y CARGAR LAS 4 MATRICES ---
    try:
        with open(nombre_archivo_entrada, 'r') as f:
            bloques = f.read().strip().split('\n\n')
        
        if len(bloques) < 4:
            print("Error: El archivo de entrada debe tener 4 matrices (Suelo, Altitud, Ea, Pq).")
            return

        # Cargamos las matrices
        # Matriz 0: Suelos (String para poder usar 'f' y '1')
        A_terreno = np.array([linea.split() for linea in bloques[0].split('\n')], dtype=str)
        # Matriz 1: Altitud (Float)
        A_altitud = np.array([linea.split() for linea in bloques[1].split('\n')], dtype=float)
        # Matriz 2: Resistencias/Ea (Float)
        A_resistencias = np.array([linea.split() for linea in bloques[2].split('\n')], dtype=float)
        # Matriz 3: Potencial/Pq (Float)
        A_potencial = np.array([linea.split() for linea in bloques[3].split('\n')], dtype=float)

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    tabla_beta = {
    '0':  [None], #terreno urbano 
    '91': [None], # Urbano
    '92': [None], # Roca
    '93': [None], # Agua
    '94': [None], # Humedales
    '95': [None], # Agua profunda
    '96': [None], # Nieve
    '97': [None], # Otros
    '98': [None], # Quemado
    '99': [None], # Genérico NB
    # MODELOS TIPO PASTIZAL (GR)
    '101': [0.00143], # GR1
    '102': [0.00158], # GR2
    '103': [0.00143], # GR3
    '104': [0.00154], # GR4
    '105': [0.00277], # GR5
    '106': [0.00335], # GR6
    '107': [0.00306], # GR7
    '108': [0.00316], # GR8
    '109': [0.00316], # GR9

    # MODELOS TIPO PASTIZAL-MATORRAL (GS)
    '121': [0.00215], # GS1
    '122': [0.00249], # GS2
    '123': [0.00259], # GS3
    '124': [0.00874], # GS4

    # MODELOS TIPO MATORRAL (SH)
    '141': [0.00280], # SH1
    '142': [0.01198], # SH2
    '143': [0.00577], # SH3
    '144': [0.00227], # SH4
    '145': [0.00206], # SH5
    '146': [0.00412], # SH6
    '147': [0.00344], # SH7
    '148': [0.00509], # SH8
    '149': [0.00505], # SH9

    # MODELOS TIPO MADERA-SOTOBOSQUE (TU)
    '161': [0.00885], # TU1
    '162': [0.00603], # TU2
    '163': [0.00359], # TU3
    '164': [0.01865], # TU4
    '165': [0.02009], # TU5

    # MODELOS TIPO HOJARASCA-SOTOBOSQUE (TL)
    '181': [0.04878], # TL1
    '182': [0.04232], # TL2
    '183': [0.02630], # TL3
    '184': [0.02224], # TL4
    '185': [0.01925], # TL5
    '186': [0.02296], # TL6
    '187': [0.03515], # TL7
    '188': [0.03969], # TL8
    '189': [0.03372], # TL9

    # MODELOS TIPO MADERA DERRIBADA (SB)
    '201': [0.02224], # SB1
    '202': [0.01829], # SB2
    '203': [0.01345], # SB3
    '204': [0.00744], # SB4
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
    
    while np.any(A_terreno == 'f'):  # Mientras haya fuego activo ('0')
        A_terreno_nueva = A_terreno.copy()
        
        # Encontrar celdas quemando ('0')
        quemando = np.where(A_terreno == 'f')
        for i, j in zip(quemando[0], quemando[1]):
            # Para cada dirección de propagación
            for (di, dj), dist in zip(direcciones, distancias):
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and A_terreno[ni, nj] not in ['f', '1', '0', '91', '92', '93', '94', '95', '96', '97', '98', '99']:
                    # Calcular la pendiente en esta dirección específica
                    # tan(φ) = dz / distancia_horizontal

                    dz = A_altitud[ni, nj] - A_altitud[i, j]
                    tan_phi = dz / dist  # Puede ser positivo (subida) o negativo (bajada)

                    # Obtener beta según el tipo de terreno en la celda destino
                    tipo_terreno = A_terreno[ni, nj]
                    beta = tabla_beta.get(tipo_terreno, [None])[0]

                    if tan_phi <= 0 or beta is None:
                        # Terreno plano, bajada o beta indefinido: no se aplica factor adicional
                        phi_s = 1
                    else:
                        # Terreno en subida y beta definido: incrementa el potencial
                        phi_s = 1 + (5.275 * (beta ** (-0.3)) * (tan_phi ** 2))

                    # Potencial efectivo con factor de pendiente
                    potencial_efectivo = A_potencial[ni, nj] * phi_s
                    
                    # Comparar potencial efectivo con resistencia
                    if  A_resistencias[ni, nj] - potencial_efectivo <= 0:
                        A_terreno_nueva[ni, nj] = 'f'  # Se quema
                    else:
                        A_resistencias[ni, nj] = A_resistencias[ni, nj] - potencial_efectivo
        
        # Cambiar las celdas que estaban quemando ('0') a ya quemado ('1')
        A_terreno_nueva[A_terreno == 'f'] = '98'
        
        A_terreno = A_terreno_nueva
        A_terreno_list.append(A_terreno.copy())
        
        # Si no hay cambios nuevos, salir
        if not np.any(A_terreno == 'f'):
            break
    
    # --- 4. GUARDAR RESULTADOS CON FORMATO SOLICITADO ---
    def formatear_matriz(matriz):
        return "\n".join([" ".join(map(str, fila)) for fila in matriz])

    with open(nombre_archivo_salida, 'w') as f_out:
        f_out.write(formatear_matriz(A_terreno_list[0]))
        f_out.write("\n\n")
        
        for idx, paso in enumerate(A_terreno_list[1:]):
            f_out.write(formatear_matriz(paso))
            f_out.write("\n\n")

    print(f"Simulación finalizada. Resultados en '{nombre_archivo_salida}'")

# Ejemplo de llamada:
#avance_fuego('salida.txt', 'evolucion_fuego.txt')