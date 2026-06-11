import numpy as np
import os

def leer_asc(ruta_archivo):
    header = {}
    with open(ruta_archivo, 'r') as f:
        for i in range(6):
            linea = f.readline().split()
            if len(linea) < 2: continue
            header[linea[0].lower()] = float(linea[1])
    
    datos = np.loadtxt(ruta_archivo, skiprows=6)
    return datos, int(header['nrows']), int(header['ncols'])

def formatear_matriz(matriz):
    # Esto genera filas de números limpios separados por espacios
    lineas = []
    for fila in matriz:
        # Convertimos a int para quitar el .0 y luego a string unidos por espacio
        linea_texto = " ".join(map(str, fila.astype(int)))
        lineas.append(linea_texto)
    return "\n".join(lineas)

def ejecutar_proceso(archivo1, archivo2, salida_txt):
    # 1. Cargar datos
    if not os.path.exists(archivo1) or not os.path.exists(archivo2):
        print("Error: No se encuentran los archivos .asc")
        return

    m1, f1, c1 = leer_asc(archivo1)
    m2, f2, c2 = leer_asc(archivo2)

    # 2. Validar dimensiones y mostrar en consola
    if f1 != f2 or c1 != c2:
        # Esto detiene la ejecución y lanza el error solicitado
        raise ValueError(f"ERROR: Dimensiones desiguales. Mapa1:({f1}x{c1}) Mapa2:({f2}x{c2})")
    
    # Si son iguales, imprimimos la info en consola
    print(f"Dimensiones detectadas:")
    print(f"Filas: {f1}")
    print(f"Columnas: {c1}")

    # 3. Escribir SOLO las matrices en el archivo TXT
    with open(salida_txt, 'w') as f:
        f.write(formatear_matriz(m1))
        f.write("\n\n") # Separación entre matrices
        f.write(formatear_matriz(m2))

    print(f"\nLas matrices han sido guardadas en: {salida_txt}")

# --- CONFIGURACIÓN ---
ejecutar_proceso('recortes_suelo_ciudadB.asc', 'recortes_alt_ciudad.asc', 'matrices_ciudad.txt')