import numpy as np
# Añade esto al principio del archivo, después de los imports
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def calcular_F_1(A_original, nombre_archivo_salida, wx, wy):
    """
    Calcula la lista de matrices F desde el estado inicial en A hasta que no haya más fuego activo.
    
    Parámetros:
    A_original: matriz del mapa inicial (letras b, c, p, s indicando tipo de terreno)
    
    Retorna:
    F_list: lista de matrices del estado del fuego en cada paso temporal
    """
    A_original = np.array(A_original)
    n, m = A_original.shape
    probabilidades = {
        'b': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
        'c': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
        'p': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
        's': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
        't': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3}
    }
    # Pedir coordenadas del fuego inicial
    x = int(input(f"¿En qué fila quieres que empiece el fuego? (0-{n-1}): "))
    y = int(input(f"¿En qué columna quieres que empiece el fuego? (0-{m-1}): "))
    
    # Validar que las coordenadas están dentro del rango
    if not (0 <= x < n and 0 <= y < m):
        print(f"Error: las coordenadas deben estar dentro de [0-{n-1}, 0-{m-1}]")
        exit()


    wind_mag = np.hypot(wx, wy)
    if wind_mag > 0:
        # Normalizamos el vector para que solo indique dirección
        wind_dir = (wx / wind_mag, wy / wind_mag)
    else:
        wind_dir = (0.0, 0.0)
    
    A = A_original.copy()  # A es el mapa de terrenos
    F = A.copy()  # F es el estado del fuego
    F[x, y] = 'f'
    
    F_list = [F.copy()]
    F_actual = F.copy()
    
    while np.any(F_actual == 'f'):
        F_1 = F_actual.copy()
        rows, cols = A.shape
        
        # Direcciones adyacentes (arriba, abajo, izquierda, derecha)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Incluyendo diagonales
        
        # Para cada celda con fuego en F_actual
        for i in range(rows):
            for j in range(cols):
                if F_actual[i, j] == 'f':  # Si hay fuego en esta celda
                    terreno_origen = A[i, j]
                    
                    # Propagar a las celdas adyacentes
                    for di, dj in direcciones:
                        ni, nj = i + di, j + dj
                        
                        # Comprobar que está dentro de los límites
                        if 0 <= ni < rows and 0 <= nj < cols:
                            terreno_destino = A[ni, nj]
                            
                            # Comprovar si la celda destino ya está quemada o con fuego
                            if F_actual[ni, nj] == 'q' or F_1[ni, nj] == 'f':
                                continue
                            
                            # Obtener la probabilidad de propagación
                            prob = probabilidades[terreno_origen].get(terreno_destino, 0.0)
                            
                            if 0 <= ni < rows and 0 <= nj < cols:
                                terreno_destino = A[ni, nj]
                                
                                if F_actual[ni, nj] == 'q' or F_1[ni, nj] == 'f':
                                    continue
                                
                                # 1. Obtener probabilidad base
                                prob = probabilidades[terreno_origen].get(terreno_destino, 0.0)
                                
                                # --- NUEVO: Ajustar por viento ---
                                if wind_mag > 0:
                                    dir_mag = np.hypot(di, dj) # Longitud del salto (1 o 1.41)
                                    # Producto escalar: (VientoX * SaltoX) + (VientoY * SaltoY)
                                    # Importante: dj es X (columnas), di es Y (filas)
                                    alineacion = (wind_dir[0] * (dj/dir_mag)) + (wind_dir[1] * (di/dir_mag))
                                    
                                    # Aplicamos el factor (puedes multiplicar wind_mag por 1.5 si quieres más efecto)
                                    factor_viento = 1 + (alineacion * wind_mag)
                                    prob = np.clip(prob * factor_viento, 0.0, 1.0)

                                    
                            if np.random.random() < prob:
                                F_1[ni, nj] = 'f'
        
        for i in range(rows):
            for j in range(cols):
                if F_actual[i, j] == 'f': # Si había fuego en esta celda, ahora se quema
                    F_1[i, j] = 'q'
        
        F_actual = F_1
        F_list.append(F_actual.copy())
    
    # Guardar las matrices en un archivo .txt
    with open(nombre_archivo_salida, 'w') as f:
        f.write(str(A_original))
        f.write("\n\n")
        
        for idx, F in enumerate(F_list):
            f.write(str(F))
            f.write("\n\n")
    
    with open(nombre_archivo_salida, 'w') as f:
        f.write(str(A_original))
        f.write("\n\n")
        
        for idx, F in enumerate(F_list):
            f.write(str(F))
            f.write("\n\n")
    
    print(f"Las matrices se han guardado en '{nombre_archivo_salida}'")


