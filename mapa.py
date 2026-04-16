import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import re
import os

def generar_video_incendio(archivo_txt, nombre_salida, wx=0, wy=0):
    # Asegurarnos de que el nombre tenga una extensión válida
    if not nombre_salida.endswith(('.mp4')):
        nombre_salida += ".mp4"

    # 1. Configuración de tipos de suelo
    suelos_info = {
        'p': {'id': 0, 'label': 'Poblado', 'color': 'dimgray'},
        'b': {'id': 1, 'label': 'Bosque', 'color': "#0d3604"},
        'c': {'id': 2, 'label': 'Cultivos', 'color': 'gold'},
        's': {'id': 3, 'label': 'Zona Segura', 'color': 'deepskyblue'},
        'q': {'id': 4, 'label': 'Zona Quemada', 'color': 'black'},
        'f': {'id': 5, 'label': 'Fuego Activo', 'color': 'red'},
        't': {'id': 6, 'label': 'Pradera', 'color': "#5ca44c"}
    }

    # 2. Leer archivo
    if not os.path.exists(archivo_txt):
        print(f"Error: No se encuentra el archivo {archivo_txt}")
        return

    with open(archivo_txt, 'r') as f:
        contenido = f.read().strip()

    bloques_matrices = contenido.split('\n\n')
    matrices_numericas = []

    for bloque in bloques_matrices:
        filas_texto = bloque.strip().split('\n')
        matriz_paso = []
        for fila in filas_texto:
            caracteres = re.findall(r'[pbcsvqft]', fila)
            if caracteres:
                fila_num = [suelos_info[c]['id'] for c in caracteres]
                matriz_paso.append(fila_num)
        
        if matriz_paso:
            matrices_numericas.append(np.array(matriz_paso))

    if not matrices_numericas:
        print("No se encontraron matrices válidas.")
        return

    filas, columnas = matrices_numericas[0].shape

    # 3. Configuración visual
    colores_lista = [info['color'] for info in suelos_info.values()]
    cmap_personalizado = mcolors.ListedColormap(colores_lista)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Crear la imagen inicial
    im = ax.imshow(matrices_numericas[0], cmap=cmap_personalizado, vmin=0, vmax=6)
    ax.grid(which='major', axis='both', linestyle='-', color='white', linewidth=1)
    ax.set_xticks(np.arange(-.5, columnas, 1))
    ax.set_yticks(np.arange(-.5, filas, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    parches = [mpatches.Patch(color=info['color'], label=info['label']) for info in suelos_info.values()]
    ax.legend(handles=parches, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if wx != 0 or wy != 0:
        # Dibujamos la flecha en la esquina inferior izquierda (coordenadas relativas al eje 0,0 a 1,1)
        # La flecha apunta en la dirección del viento (wx, wy)
        ax.annotate('', xy=(0.1, 0.1), xycoords='axes fraction',
                    xytext=(0.1 - wx*0.05, 0.1 - wy*0.05), textcoords='axes fraction',
                    arrowprops=dict(facecolor='white', edgecolor='white', headwidth=10, width=3),
                    label='Dirección Viento')
        # Añadimos una etiqueta de texto pequeña
        ax.text(0.05, 0.02, 'Viento', transform=ax.transAxes, color='white', fontsize=10, fontweight='bold')

        
    def update(frame):
        ax.set_title(f"Simulación de Propagación de Fuego - Paso {frame}", fontsize=16)
        im.set_array(matrices_numericas[frame])
        return [im]


    ani = FuncAnimation(fig, update, frames=len(matrices_numericas), interval=1000, blit=False)
    plt.subplots_adjust(top=0.88, right=0.8)
    # 4. Guardar directamente como MP4 , libreria ffmpeg
    print(f"Generando video MP4: {nombre_salida}...")
    writer = FFMpegWriter(fps=1)
    ani.save(nombre_salida, writer=writer)
    print("¡Proceso finalizado con éxito!")
#generar_video_incendio("test2.txt", "videotest2")