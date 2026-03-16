import numpy as np

#sea 1 bosque, 2 cultivo, 3 població, 4 zona segura
#sea la probabilidad de que el fuego pase de 1 a 1: 0.8, que pase de 1 a 2: 0.7, de 1 a 3: 0.5, de 1 a 4:0, de 2 a 2: 0.5, de 2 a 3: 0.4, de 2 a 4: 0, de 3 a 3: 0.2, de 3 a 4: 0 i de 4 a 4: 0

# Pedir las dimensiones del mapa
n = int(input("¿Cuántas filas quieres que tenga el mapa? "))
m = int(input("¿Cuántas columnas quieres que tenga el mapa? "))

# Preguntar si quiere un mapa aleatorio o introducirlo manualmente
opcion = input("¿Quieres que el mapa sea aleatorio (a) o quieres introducirlo manualmente (m)? (a/m): ").lower()

if opcion == 'a':
    # Crear mapa aleatorio con valores b, c, p, s (bosque, cultivo, población, zona segura)
    A = np.random.choice(['b', 'c', 'p', 's'], size=(n, m))
elif opcion == 'm':
    # Introducir mapa manualmente
    A = np.empty((n, m), dtype=str)
    print(f"Introduce los valores del mapa {n}x{m} (valores b, c, p, s):")
    print("Para cada fila, introduce las letras encadenadas sin espacios (ej: bcps para una fila de 4 columnas)")
    for i in range(n):
        while True:
            try:
                fila_str = input(f"Fila {i}: ")
                # Verificar que la longitud coincida
                if len(fila_str) != m:
                    print(f"Error: debes introducir exactamente {m} letras")
                    continue
                # Verificar que todos sean letras válidas
                if not all(c in 'bcps' for c in fila_str):
                    print("Error: solo se aceptan letras b, c, p, s")
                    continue
                # Asignar a la fila
                for j, letra in enumerate(fila_str):
                    A[i, j] = letra
                break
            except ValueError:
                print("Error: introduce solo letras encadenadas")
else:
    print("Error: opción no válida")
    exit()

# Pedir coordenadas del fuego inicial
x = int(input(f"¿En qué fila quieres que empiece el fuego? (0-{n-1}): "))
y = int(input(f"¿En qué columna quieres que empiece el fuego? (0-{m-1}): "))

# Validar que las coordenadas están dentro del rango
if not (0 <= x < n and 0 <= y < m):
    print(f"Error: las coordenadas deben estar dentro de [0-{n-1}, 0-{m-1}]")
    exit()

# 'f' significa que hay fuego, letra del terreno significa que no hay fuego, 'q' que ya está quemado.
F_0 = A.copy()
F_0[x, y] = 'f'

# Matriz de probabilidades de propagación del fuego
suelos_info = {
    'p': {'id': 0, 'label': 'Poblado', 'color': 'dimgray', 'prob_quemado': 0.1},
    'b': {'id': 1, 'label': 'Bosque', 'color': 'forestgreen', 'prob_quemado': 0.8},
    'c': {'id': 2, 'label': 'Cultivos', 'color': 'gold', 'prob_quemado': 0.5},
    's': {'id': 3, 'label': 'Zona Segura', 'color': 'deepskyblue', 'prob_quemado': 0.0},
    'q': {'id': 4, 'label': 'Zona Quemada', 'color': 'black', 'prob_quemado': 0.0},
    'f': {'id': 5, 'label': 'Fuego Activo', 'color': 'red', 'prob_quemado': 1.0}
}

# Probabilidades de propagación del fuego entre terrenos
probabilidades = {
    'b': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0},
    'c': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0},
    'p': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0},
    's': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0}
}


def calcular_F_1(A, F_0):
    """
    Calcula F_1 basado en F_0 y las probabilidades de propagación del fuego.
    
    Parámetros:
    A: matriz del mapa (letras b, c, p, s indicando tipo de terreno)
    F_0: matriz del estado inicial del fuego (letras del terreno, 'f'=fuego, 'q'=quemado)
    
    Retorna:
    F_1: matriz del estado del fuego después de 1 paso temporal
    """
    F_1 = F_0.copy()
    rows, cols = A.shape
    
    # Direcciones adyacentes (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Para cada celda con fuego en F_0
    for i in range(rows):
        for j in range(cols):
            if F_0[i, j] == 'f':  # Si hay fuego en esta celda
                terreno_origen = A[i, j]
                
                # Propagar a las celdas adyacentes
                for di, dj in direcciones:
                    ni, nj = i + di, j + dj
                    
                    # Comprobar que está dentro de los límites
                    if 0 <= ni < rows and 0 <= nj < cols:
                        terreno_destino = A[ni, nj]
                        
                        # Comprovar si la celda destino ya está quemada o con fuego
                        if F_0[ni, nj] == 'q' or F_1[ni, nj] == 'f':
                            continue
                        
                        # Obtener la probabilidad de propagación
                        prob = probabilidades[terreno_origen].get(terreno_destino, 0.0)
                        
                        # Aplicar la probabilidad (usando probabilidad)
                        if np.random.random() < prob:
                            F_1[ni, nj] = 'f'
    
    for i in range(rows):
        for j in range(cols):
            if F_0[i, j] == 'f': # Si había fuego en esta celda, ahora se quema
                F_1[i, j] = 'q'
    
    return F_1

# Calcular F_n hasta que no haya más fuego activo (solo letras del terreno y 'q')
F_actual = F_0.copy()
F_list = [F_0.copy()]
while np.any(F_actual == 'f'):
    F_actual = calcular_F_1(A, F_actual)
    F_list.append(F_actual.copy())

# Guardar las matrices en un archivo .txt
with open('matrices.txt', 'w') as f:
    f.write(str(A))
    f.write("\n")
    
    for idx, F in enumerate(F_list):
        f.write(str(F))
        f.write("\n")

print("Las matrices se han guardado en 'matrices.txt'")
