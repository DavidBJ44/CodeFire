import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np

# 1. Definición de la configuración de tipos de suelo
# Aquí asociamos cada letra a un número, un color y un nombre
suelos_info = {
    'p': {'id': 0, 'label': 'Poblado', 'color': 'dimgray'},
    'b': {'id': 1, 'label': 'Bosque', 'color': 'forestgreen'},
    'c': {'id': 2, 'label': 'Cultivos', 'color': 'gold'},
    's': {'id': 3, 'label': 'Zona Segura', 'color': 'deepskyblue'},
    'q': {'id': 4, 'label': 'Zona Quemada', 'color': 'black'},
    'f': {'id': 5, 'label': 'Fuego Activo', 'color': 'red'} # Opcional, por si lo necesitas
}

# 2. Tu matriz de ejemplo (puedes sustituirla por la evolución de tu código)
# Supongamos que esta es la matriz resultante de tu simulación
mapa_letras = [
    ['b', 'b', 'b', 's', 's'],
    ['b', 'f', 'b', 's', 's'],
    ['c', 'q', 'p', 'p', 'b'],
    ['c', 'c', 'p', 'p', 'b'],
    ['s', 's', 'b', 'b', 'b']
]

# 3. Convertir matriz de letras a matriz numérica para que Matplotlib la entienda
filas = len(mapa_letras)
columnas = len(mapa_letras[0])
matriz_numerica = np.zeros((filas, columnas))

for i in range(filas):
    for j in range(columnas):
        letra = mapa_letras[i][j]
        matriz_numerica[i][j] = suelos_info[letra]['id']

# 4. Configurar colores para la visualización
colores_lista = [info['color'] for info in suelos_info.values()]
cmap_personalizado = mcolors.ListedColormap(colores_lista)

# 5. Crear la figura
plt.figure(figsize=(10, 7))

# Mostrar la matriz
# vmin y vmax aseguran que los colores no cambien si falta algún tipo de suelo
im = plt.imshow(matriz_numerica, cmap=cmap_personalizado, vmin=0, vmax=len(suelos_info)-1)

# Añadir una cuadrícula (grid) para que se vea la división de la matriz
plt.grid(which='major', axis='both', linestyle='-', color='white', linewidth=1)
plt.xticks(np.arange(-.5, columnas, 1), []) # Ocultar números de ejes
plt.yticks(np.arange(-.5, filas, 1), [])

# 6. CREAR LA LEYENDA PERSONALIZADA
parches = [mpatches.Patch(color=info['color'], label=info['label']) for info in suelos_info.values()]
plt.legend(handles=parches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=12)

plt.title("Simulación de Propagación de Fuego", fontsize=16, pad=20)
plt.tight_layout() # Para que la leyenda no se corte
plt.show()