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
    # MODELOS TIPO PASTIZAL (GR) - Amarillos

        '101': {'id': 0, 'label': 'GR1', 'color': '#FFFFE0'},
        '102': {'id': 1, 'label': 'GR2', 'color': '#FFFACD'},
        '103': {'id': 2, 'label': 'GR3', 'color': '#FFF59D'},
        '104': {'id': 3, 'label': 'GR4', 'color': '#FFEE58'},
        '105': {'id': 4, 'label': 'GR5', 'color': '#FDD835'},
        '106': {'id': 5, 'label': 'GR6', 'color': '#FBC02D'},
        '107': {'id': 6, 'label': 'GR7', 'color': '#F9A825'},
        '108': {'id': 7, 'label': 'GR8', 'color': '#F57F17'},
        '109': {'id': 8, 'label': 'GR9', 'color': '#E65100'},
    # MODELOS TIPO PASTIZAL-MATORRAL (GS) - Naranjas
        '121': {'id': 9, 'label': 'GS1', 'color':  '#FFCC80'},
        '122': {'id': 10, 'label': 'GS2', 'color': '#FFB74D'},
        '123': {'id': 11, 'label': 'GS3', 'color': '#FFA726'},
        '124': {'id': 12, 'label': 'GS4', 'color': '#FB8C00'},
    # MODELOS TIPO MATORRAL (SH) - Verdes Claros
        '141': {'id': 13, 'label': 'SH1', 'color': '#E8F5E9'},
        '142': {'id': 14, 'label': 'SH2', 'color': '#C8E6C9'},
        '143': {'id': 15, 'label': 'SH3', 'color': '#A5D6A7'},
        '144': {'id': 16, 'label': 'SH4', 'color': '#81C784'},
        '145': {'id': 17, 'label': 'SH5', 'color': '#66BB6A'},
        '146': {'id': 18, 'label': 'SH6', 'color': '#4CAF50'},
        '147': {'id': 19, 'label': 'SH7', 'color': '#43A047'},
        '148': {'id': 20, 'label': 'SH8', 'color': '#388E3C'},
        '149': {'id': 21, 'label': 'SH9', 'color': "#E6E6E6"},
    # MODELOS BOSQUE: MADERA-SOTOBOSQUE (TU) - Verdes Oscuros / Oliva
        '161': {'id': 22, 'label': 'TU1', 'color': '#556B2F'},
        '162': {'id': 23, 'label': 'TU2', 'color': '#4B5320'},
        '163': {'id': 24, 'label': 'TU3', 'color': '#3D441E'},
        '164': {'id': 25, 'label': 'TU4', 'color': '#2E3316'},
        '165': {'id': 26, 'label': 'TU5', 'color': '#1F220E'},
    # MODELOS BOSQUE: HOJARASCA (TL) - Verdes Oscuros Azulados
        '181': {'id': 27, 'label': 'TL1', 'color': '#2E7D32'},
        '182': {'id': 28, 'label': 'TL2', 'color': '#1B5E20'},
        '183': {'id': 29, 'label': 'TL3', 'color': '#004D40'},
        '184': {'id': 30, 'label': 'TL4', 'color': '#00332E'},
        '185': {'id': 31, 'label': 'TL5', 'color': '#00251A'},
        '186': {'id': 32, 'label': 'TL6', 'color': '#1A237E'},
        '187': {'id': 33, 'label': 'TL7', 'color': '#0D47A1'},
        '188': {'id': 34, 'label': 'TL8', 'color': '#01579B'},
        '189': {'id': 35, 'label': 'TL9', 'color': "#002C04"},
    # MODELOS MADERA DERRIBADA (SB) - Marrones/Tierras (por ser restos muertos)
        '201': {'id': 36, 'label': 'SB1', 'color': '#D7CCC8'},
        '202': {'id': 37, 'label': 'SB2', 'color': '#A1887F'},
        '203': {'id': 38, 'label': 'SB3', 'color': '#795548'},
        '204': {'id': 39, 'label': 'SB4', 'color': '#3E2723'},
        # Especiales
        'f': {'id': 41, 'label': 'Fuego Activo', 'color': 'red'},
        '0': {'id': 42, 'label': 'Agua', 'color': "#3030AC"},
    # MODELOS NO COMBUSTIBLES (NB - Non-Burnable)
        '91': {'id': 43, 'label': 'NB1', 'color': '#424242'}, # Urbano/Infraestructuras (Asfalto, edificios)
        '92': {'id': 44, 'label': 'NB2', 'color': '#E0E0E0'}, # Suelo desnudo (Roca, arena, canteras)
        '93': {'id': 45, 'label': 'NB3', 'color': '#3030AC'}, # Agua (Ríos, lagos, canales, mar)
        '94': {'id': 46, 'label': 'NB4', 'color': '#3030AC'}, # Zonas húmedas (Tierras bajas inundadas, humedales)
        '95': {'id': 47, 'label': 'NB5', 'color': '#3030AC'}, # Agua profunda / Masas de agua permanentes
        '96': {'id': 48, 'label': 'NB6', 'color': '#FFFFFF'}, # Nieve / Hielo (Cumbres nevadas o glaciares)
        '97': {'id': 49, 'label': 'NB7', 'color': '#BDBDBD'}, # Otros (Uso genérico para huecos sin datos)
        '98': {'id': 50, 'label': 'Quemado (NB8)', 'color': '#212121'}, # Terreno quemado recientemente (sin vegetación)
        '99': {'id': 51, 'label': 'NB9', 'color': '#757575'}, # Código genérico de "No Combustible"
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
            caracteres = fila.split()
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
    
    fig, ax = plt.subplots(figsize=(12, 9))
    
    # Crear la imagen inicial
    im = ax.imshow(matrices_numericas[0], cmap=cmap_personalizado, vmin=0, vmax=51)
    ax.grid(which='major', axis='both', linestyle='-', color='white', linewidth=0.2)
    ax.set_xticks(np.arange(-.5, columnas, 1))
    ax.set_yticks(np.arange(-.5, filas, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    parches = [mpatches.Patch(color=info['color'], label=info['label']) for info in suelos_info.values()]
    ax.legend(handles=parches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2)
    
    if wx != 0 or wy != 0:
        # 1. Definimos la posición base (Centro del lateral izquierdo)
        # x=0.05 está muy cerca del borde izquierdo, y=0.5 es la mitad de la altura
        base_x, base_y = -0.20, 0.5 
        
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
                        headwidth=8,   # Punta más ancha
                        width=4,        # Cuerpo más grueso
                        alpha=0.9       # Casi opaco para que se vea bien
                    ))
        
        # 4. Texto "Viento" en rojo y un poco más grande
        ax.text(base_x, base_y - 0.08, 'Direcció Vent', 
                transform=ax.transAxes, 
                color='red', 
                fontsize=12, 
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
    plt.subplots_adjust(top=0.88, right=0.8, left=0.25)

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
#ejemplo uso 
#generar_video_incendio('evolucion_fuego.txt','mat_text_out',1,1)