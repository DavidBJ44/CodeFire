import numpy as np

#sea 1 bosque, 2 cultivo, 3 població, 4 zona segura
#sea la probabilidad de que el fuego pase de 1 a 1: 0.8, que pase de 1 a 2: 0.7, de 1 a 3: 0.5, de 1 a 4:0, de 2 a 2: 0.5, de 2 a 3: 0.4, de 2 a 4: 0, de 3 a 3: 0.2, de 3 a 4: 0 i de 4 a 4: 0

# Pedir las dimensiones del mapa
n = int(input("¿Cuántas filas quieres que tenga el mapa? "))
m = int(input("¿Cuántas columnas quieres que tenga el mapa? "))

# Preguntar si quiere un mapa aleatorio o introducirlo manualmente
opcion = input("¿Quieres que el mapa sea aleatorio (a) o quieres introducirlo manualmente (m)? (a/m): ").lower()

if opcion == 'a':
    # Crear mapa aleatorio con valores 1-4 (bosque, cultivo, población, zona segura)
    A = np.random.randint(1, 5, size=(n, m))
elif opcion == 'm':
    # Introducir mapa manualmente
    A = np.zeros((n, m), dtype=int)
    print(f"Introduce los valores del mapa {n}x{m} (valores 1-4):")
    print("Para cada fila, introduce los números encadenados sin espacios (ej: 1234 para una fila de 4 columnas)")
    for i in range(n):
        while True:
            try:
                fila_str = input(f"Fila {i}: ")
                # Verificar que la longitud coincida
                if len(fila_str) != m:
                    print(f"Error: debes introducir exactamente {m} números")
                    continue
                # Verificar que todos sean números del 1 al 4
                if not all(c in '1234' for c in fila_str):
                    print("Error: solo se aceptan números del 1 al 4")
                    continue
                # Convertir a números y asignar a la fila
                for j, valor_str in enumerate(fila_str):
                    A[i, j] = int(valor_str)
                break
            except ValueError:
                print("Error: introduce solo números encadenados")
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

#1 significa que hay fuego i 0 significa que no.
F_0 = np.zeros((n, m), dtype=int)
F_0[x, y] = 1

# Matriz de probabilidades de propagación del fuego
# probabilidades[terreno_origen][terreno_destino] = probabilidad
probabilidades = {
    1: {1: 0.8, 2: 0.7, 3: 0.5, 4: 0.0},  # de bosque
    2: {2: 0.5, 3: 0.4, 4: 0.0},          # de cultivo
    3: {3: 0.2, 4: 0.0},                  # de población
    4: {4: 0.0}                           # de zona segura
}

def calcular_F_1(A, F_0):
    """
    Calcula F_1 basado en F_0 y las probabilidades de propagación del fuego.
    
    Parámetros:
    A: matriz del mapa (valores 1-4 indicando tipo de terreno)
    F_0: matriz del estado inicial del fuego (1=fuego, 0=sin fuego)
    
    Retorna:
    F_1: matriz del estado del fuego después de 1 paso temporal
    """
    F_1 = F_0.copy().astype(float)
    rows, cols = A.shape
    
    # Direcciones adyacentes (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Para cada celda con fuego en F_0
    for i in range(rows):
        for j in range(cols):
            if F_0[i, j] == 1:  # Si hay fuego en esta celda
                terreno_origen = A[i, j]
                
                # Propagar a las celdas adyacentes
                for di, dj in direcciones:
                    ni, nj = i + di, j + dj
                    
                    # Comprobar que está dentro de los límites
                    if 0 <= ni < rows and 0 <= nj < cols:
                        terreno_destino = A[ni, nj]
                        
                        # Obtener la probabilidad de propagación
                        if terreno_origen in probabilidades:
                            prob = probabilidades[terreno_origen].get(terreno_destino, 0.0)
                        else:
                            prob = 0.0
                        
                        # Aplicar la probabilidad (usando probabilidad)
                        if np.random.random() < prob:
                            F_1[ni, nj] = 1
    
    return F_1.astype(int)

# Pedir al usuario el número de pasos
n = int(input("¿Cuántos pasos temporal quieres simular? "))

# Calcular F_n iterando n veces
F_actual = F_0.copy()
for paso in range(n):
    F_actual = calcular_F_1(A, F_actual)

print("Mapa (A):")
print(A)
print("\nEstado inicial del fuego (F_0):")
print(F_0)
print(f"\nEstado del fuego después de {n} pasos (F_{n}):")
print(F_actual)
