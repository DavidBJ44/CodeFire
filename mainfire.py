from mapa import generar_video_incendio
from fire2 import calcular_F_1
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import re
import os

# Variable global para "recordar" la matriz
matriz_guardada = None

suelos_info = {
    'p': {'id': 0, 'label': 'Poblado', 'color': 'dimgray'},
    'b': {'id': 1, 'label': 'Bosque', 'color': "#0d3604"},
    'c': {'id': 2, 'label': 'Cultivos', 'color': 'gold'},
    's': {'id': 3, 'label': 'Zona Segura', 'color': 'deepskyblue'},
    'q': {'id': 4, 'label': 'Zona Quemada', 'color': 'black'},
    'f': {'id': 5, 'label': 'Fuego Activo', 'color': 'red'},
    't': {'id': 6, 'label': 'Pradera', 'color': "#5ca44c"}
}

# Probabilidades de propagación del fuego entre terrenos
probabilidades = {
     'b': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
    'c': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
    'p': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
    's': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3},
    't': {'b': 0.8, 'c': 0.5, 'p': 0.1, 's': 0.0, 't': 0.3}

}
def leerm(nombre_archivo):
    global matriz_guardada
    
    try:
        with open(nombre_archivo, 'r') as f:
            contenido = f.read().strip()

        # 1. Detectar si hay más de una matriz utilizando expresiones regulares
        # Buscamos el patrón [[ ... ]]
        matrices_encontradas = re.findall(r'\[\[.*?\]\]', contenido, re.DOTALL)
        
        if len(matrices_encontradas) > 1:
            raise Exception("Error: Se ha detectado más de una matriz en el archivo.")
        if len(matrices_encontradas) == 0:
            raise Exception("Error: No se encontró ninguna matriz con el formato [[...]].")

        # 2. Procesar la matriz encontrada
        texto_matriz = matrices_encontradas[0]
        
        # Limpiamos los corchetes exteriores e interiores para obtener solo los datos
        # Reemplazamos '[' y ']' por nada y dividimos por líneas
        filas_limpias = texto_matriz.replace('[[', '').replace(']]', '').split('\n')
        
        temp_matriz = []
        for fila in filas_limpias:
            # Quitamos corchetes de la fila y espacios extra
            elementos = fila.replace('[', '').replace(']', '').strip().split()
            
            if not elementos: # Saltar líneas vacías si las hay
                continue
                
            # Validar que los caracteres existan en el diccionario
            for char in elementos:
                if char not in suelos_info:
                    raise ValueError(f"Error: Carácter '{char}' no reconocido en el diccionario.")
            
            temp_matriz.append(elementos)

        # 3. Validar dimensiones (que sea nxm real)
        n = len(temp_matriz)
        m = len(temp_matriz[0]) if n > 0 else 0
        
        if not all(len(fila) == m for fila in temp_matriz):
            raise Exception("Error: La matriz no tiene un tamaño uniforme (n x m).")

        # 4. Guardar en la variable global para "recordarla"
        matriz_guardada = temp_matriz
        
        print(f"Matriz cargada exitosamente. Tamaño detectado: {n}x{m}")
        return n, m

    except FileNotFoundError:
        print("Error: El archivo no existe.")
    except Exception as e:
        print(f"Error al leer la matriz: {e}")

leerm("test10x10.txt")
calcular_F_1 (matriz_guardada)
generar_video_incendio("test10.txt", "prueba1")