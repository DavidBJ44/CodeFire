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

                    if tan_phi <= 0:
                        phi_s = 1  # Terreno plano o bajada: el potencial se queda igual
                    else:
                        # Terreno en subida: sumamos 1 para que el potencial aumente
                        phi_s = 1 + (5.275 * (tan_phi ** 2))
                    
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
        if not np.any(A_terreno == '0'):
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
avance_fuego('salida.txt', 'evolucion_fuego.txt')