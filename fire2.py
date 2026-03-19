import numpy as np
# Añade esto al principio del archivo, después de los imports
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def calcular_F_1(testm_temp,salida):
    """
    Calcula la lista de matrices F desde el estado inicial en A hasta que no haya más fuego activo.
    
    Parámetros:
    testm_temp: matriz del mapa inicial (letras b, c, p, s, t indicando tipo de terreno)
    
    Retorna:
    F_list: lista de matrices del estado del fuego en cada paso temporal
    """
    testm_temp = np.array(testm_temp)
    n, m = testm_temp.shape

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

    # Pedir vector de viento (componentes x,y) después de elegir la ubicación inicial del fuego
    wx = float(input("Introduce componente x del viento (derecha +, izquierda -): "))
    wy = float(input("Introduce componente y del viento (abajo +, arriba -): "))
    wind_mag = np.hypot(wx, wy) # Calcula el módulo del viento (.hypot calcula la hipotenusa)
    if wind_mag > 0:
        wind_dir = (wx / wind_mag, wy / wind_mag)
    else:
        wind_dir = (0.0, 0.0)

    A = testm_temp.copy()  # A es el mapa de terrenos
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

                            # Ajustar la probabilidad según el viento: aumenta en la dirección del viento,
                            # disminuye en dirección contraria.
                            dir_mag = np.hypot(di, dj)
                            if dir_mag > 0 and wind_mag > 0:
                                dir_vec = (di / dir_mag, dj / dir_mag)
                                alineacion = wind_dir[0] * dir_vec[0] + wind_dir[1] * dir_vec[1]
                                factor_viento = 1 + 0.5 * alineacion * min(1, wind_mag)
                                prob = np.clip(prob * factor_viento, 0.0, 1.0)

                            # Aplicar la probabilidad (usando probabilidad)
                            if np.random.random() < prob:
                                F_1[ni, nj] = 'f'
        
        for i in range(rows):
            for j in range(cols):
                if F_actual[i, j] == 'f': # Si había fuego en esta celda, ahora se quema
                    F_1[i, j] = 'q'
        
        F_actual = F_1
        F_list.append(F_actual.copy())
    
    # Guardar las matrices en un archivo .txt
    with open(salida, 'w') as f:
        f.write(str(testm_temp))
        f.write("\n\n")
        
        for idx, F in enumerate(F_list):
            f.write(str(F))
            f.write("\n\n")
    


