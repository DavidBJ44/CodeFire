import numpy as np
# Añade esto al principio del archivo, después de los imports
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

def avance_fuego(A_resistencias, A_potencial, nombre_archivo_salida, A_altitud, A_terreno):
    """
    Calcula la lista de matrices F desde el estado inicial en A hasta que no haya más fuego activo.
    
    Parámetros:
    A_resistencias: matriz de las resistencias del mapa 
    A_potencial: matriz del potencial de propagación del fuego en el mapa
    nombre_archivo_salida: nombre del fichero donde se guardan las matrices
    A_terreno: matriz de tipos de terreno ('b', 'c', 'p')
    Retorna:
    F_list: lista de matrices del estado del fuego en cada paso temporal
    """
    A_resistencias = np.array(A_resistencias, dtype=float)
    A_potencial = np.array(A_potencial, dtype=float)
    n, m = A_resistencias.shape
    
    if A_potencial.shape != (n, m):
        raise ValueError("Las matrices de resistencias y potencial deben tener la misma forma")
    
    
    A_altitud = np.array(A_altitud, dtype=float)
    if A_altitud.shape != (n, m):
        raise ValueError("La matriz de altitud debe tener la misma forma que las otras matrices")
    
    
    A_terreno = np.array(A_terreno, dtype=str)
    if A_terreno.shape != (n, m):
        raise ValueError("La matriz de terreno debe tener la misma forma que las otras matrices")
    
    cell_size = 10.0
    
    # Direcciones y sus distancias (para diagonales usamos la hipotenusa)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    distancias = [cell_size, cell_size, cell_size, cell_size, cell_size * np.sqrt(2), cell_size * np.sqrt(2), cell_size * np.sqrt(2), cell_size * np.sqrt(2)]
    
    
    if x is None or y is None:
         # Pedir coordenadas del fuego inicial
        x = int(input(f"¿En qué fila quieres que empiece el fuego? (0-{n-1}): "))
        y = int(input(f"¿En qué columna quieres que empiece el fuego? (0-{m-1}): "))
    
    # Validar que las coordenadas están dentro del rango
    if not (0 <= x < n and 0 <= y < m):
        print(f"Error: las coordenadas deben estar dentro de [0-{n-1}, 0-{m-1}]")
        return []
    
    # Inicializar matriz de terreno, cambiar inicial a quemando
    A_terreno[x, y] = '0'  # Fuego inicial quemando
    
    A_terreno_list = [A_terreno.copy()]
    
    while np.any(A_terreno == '0'):  # Mientras haya fuego activo ('0')
        A_terreno_nueva = A_terreno.copy()
        
        # Encontrar celdas quemando ('0')
        quemando = np.where(A_terreno == '0')
        for i, j in zip(quemando[0], quemando[1]):
            # Para cada dirección de propagación
            for (di, dj), dist in zip(direcciones, distancias):
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and A_terreno[ni, nj] in ['b', 'c', 'p']:  # Solo si no quemado
                    # Calcular la pendiente en esta dirección específica
                    # tan(φ) = dz / distancia_horizontal
                    dz = A_altitud[ni, nj] - A_altitud[i, j]
                    tan_phi = dz / dist  # Puede ser positivo (subida) o negativo (bajada)
                    if tan_phi < 0:
                        phi_s = 1  # No consideramos el efecto de bajada, solo subida
                    else:
                        # Fórmula de Rothermel: φ_s = 5.275 × (tan(φ))²
                        phi_s = 5.275 * (tan_phi ** 2)
                    
                    # Potencial efectivo con factor de pendiente
                    potencial_efectivo = A_potencial[ni, nj] * phi_s
                    
                    # Comparar potencial efectivo con resistencia
                    if  A_resistencias[ni, nj] - potencial_efectivo <= 0:
                        A_terreno_nueva[ni, nj] = '0'  # Se quema
                    else:
                        A_resistencias[ni, nj] = A_resistencias[ni, nj] - potencial_efectivo
        
        # Cambiar las celdas que estaban quemando ('0') a ya quemado ('1')
        A_terreno_nueva[A_terreno == '0'] = '1'
        
        A_terreno = A_terreno_nueva
        A_terreno_list.append(A_terreno.copy())
        
        # Si no hay cambios nuevos, salir
        if not np.any(A_terreno == '0'):
            break
    
    # Guardar las matrices en el archivo de salida
    with open(nombre_archivo_salida, 'w') as f:
        f.write("Resistencias:\n")
        f.write(str(A_resistencias))
        f.write("\n\nPotencial base:\n")
        f.write(str(A_potencial))
        f.write("\n\nAltitud:\n")
        f.write(str(A_altitud))
        f.write("\n\nTerreno:\n")
        f.write(str(A_terreno))
        f.write("\n\nNota: El factor de pendiente se calcula directamente en cada paso\n")
        f.write("usando la fórmula de Rothermel: φ_s = 5.275 × (tan(φ))²\n")
        f.write("donde φ es el ángulo de pendiente en la dirección específica de propagación.\n\n")
        for idx, A_terreno_paso in enumerate(A_terreno_list):
            f.write(f"Paso {idx}:\n")
            f.write(str(A_terreno_paso))
            f.write("\n\n")
    
    print(f"Las matrices se han guardado en '{nombre_archivo_salida}'")
    return A_terreno_list