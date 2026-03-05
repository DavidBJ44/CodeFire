import numpy as np

#sea 1 bosque, 2 cultivo, 3 població, 4 zona segura
#sea la probabilidad de que el fuego pase de 1 a 1: 0.8, que pase de 1 a 2: 0.7, de 1 a 3: 0.5, de 1 a 4:0, de 2 a 2: 0.5, de 2 a 3: 0.4, de 2 a 4: 0, de 3 a 3: 0.2, de 3 a 4: 0 i de 4 a 4: 0

A = np.array([
    [1,1,1,2,3],
    [1,1,4,2,2],
    [1,1,1,3,3],
    [1,1,4,3,3],
    [1,4,2,2,2]
])

#1 significa que hay fuego i 0 significa que no.

F_0 = np.array([
    [1,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
])

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

# Calcular F_1
F_1 = calcular_F_1(A, F_0)

print("Mapa (A):")
print(A)
print("\nEstado inicial del fuego (F_0):")
print(F_0)
print("\nEstado del fuego después de 1 paso (F_1):")
print(F_1)
