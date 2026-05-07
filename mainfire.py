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
# --- Pedir vector de viento ---
wx = float(input("Viento X (Izquierda -1 / Derecha +1): "))
wy = float(input("Viento Y (Abajo -1 / Arriba +1): "))

leerm("testp&v.txt")
calcular_F_1 (matriz_guardada, "testp&v2.txt", wx,wy)
generar_video_incendio("testp&v2.txt", "videop&v",wx,wy)