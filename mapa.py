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
        'T1': {'id': 0, 'label': 'Zona 1', 'color': 'dimgray'},
        'T2': {'id': 1, 'label': 'Zona 2', 'color': "#0d3604"},
        'T3': {'id': 2, 'label': 'Zona 3', 'color': 'gold'},
        'T4': {'id': 3, 'label': 'Zona Segura', 'color': 'deepskyblue'},
        'q': {'id': 4, 'label': 'Zona Quemada', 'color': 'black'},
        'f': {'id': 5, 'label': 'Fuego Activo', 'color': 'red'},
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
        # 1. Definimos la posición base (Centro del lateral izquierdo)
        # x=0.05 está muy cerca del borde izquierdo, y=0.5 es la mitad de la altura
        base_x, base_y = -0.22, 0.5 
        
        # 2. Definimos la escala (qué tan larga es la flecha)
        # Aumentamos el factor a 0.1 para que sea más grande
        escala = 0.1 
        
        # 3. Dibujamos la flecha en ROJO
        ax.annotate('', 
                    xy=(base_x + wx * escala, base_y + wy * escala), # Punta
                    xytext=(base_x, base_y),                        # Base
                    xycoords='axes fraction',
                    arrowprops=dict(
                        facecolor='red', 
                        edgecolor='red', 
                        headwidth=15,   # Punta más ancha
                        width=6,        # Cuerpo más grueso
                        alpha=0.9       # Casi opaco para que se vea bien
                    ))
        
        # 4. Texto "Viento" en rojo y un poco más grande
        ax.text(base_x, base_y - 0.12, 'Direcció Vent', 
                transform=ax.transAxes, 
                color='red', 
                fontsize=14, 
                fontweight='bold', 
                ha='center')
        
        # 5. Valores del vector (wx, wy) justo debajo
        texto_vector = f"({wx:.1f}, {wy:.1f})"
        ax.text(base_x, base_y - 0.18, texto_vector, 
                transform=ax.transAxes, 
                color='red', 
                fontsize=12, 
                ha='center',
                va='top',
                clip_on=False)
        
    # Ajustamos el margen izquierdo para que la flecha no se vea "apretada"
    plt.subplots_adjust(top=0.88, right=0.8, left=0.15)

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