import F_RP
import fire2
import mapa
import ffmc
import bui
import pandas as pd

def main():
    # --- CONFIGURACIÓN DE ARCHIVOS ---
    archivo_inicial = 'matrices_sin_pendiente.txt'    # Suelo + Altitud
    archivo_7_matrices = 'test_7Matrices.txt'        # Suelo + Altitud + Ea + Pq
    archivo_evolucion = 'test_evolucion_fuego.txt' # Pasos del fuego
    archivo_video = 'simulacion_incendio_xxxxxxxx'     # Nombre del video final (sin .mp4)
    velocidad_viento = 25 #km/h
    viento_x = 1 
    viento_y = 1
    direccion_viento = (viento_x ,viento_y)
    temp_amb = 25.3#del dia q toca caluclar 
    m=0.77 #del dia q toca calcular
    matriz_ffmc = pd.read_csv('csv/dades_inicials.csv', header=None).values
    matriz_bui = pd.read_csv('csv/dades_inicials.csv', header=None).iloc[:, :-1].values
    
    # --- 1. GENERAR DICCIONARIO Y MATRICES DE ENERGÍA (F_RP) ---
    print("=== PASO 1: Generando Diccionario de Combustibles ===")
    

    
    # Generamos el diccionario { 'ID': [ea, pq] }
    diccionario_fuego = F_RP.generar_diccionario_fuego(ffmc.calcular_ffmc(matriz_ffmc), bui.calcular_bui(matriz_bui), temp_amb,m)
   # --- ESTIU (Catalunya, Risc Extrem - Pla Alfa 3) ---
   #diccionario_fuego = F_RP.generar_diccionario_fuego(90.0, 90.0, 35.0, 0.5)

## --- PRIMAVERA (Catalunya, Humitat variable) ---
    #diccionario_fuego = F_RP.generar_diccionario_fuego(65.0, 50.0, 22.0, 0.75)
#
## --- TARDOR (Catalunya, Post-estiu sec) ---
    #diccionario_fuego = F_RP.generar_diccionario_fuego(45.0, 45.0, 18.0, 0.55)
#
## --- HIVERN (Catalunya, Fred i humit) ---
   # diccionario_fuego = F_RP.generar_diccionario_fuego(20.0, 10.0, 9.0, 0.85)

    # Generamos el archivo que combina las 4 matrices necesarias
    F_RP.Gen_e_q_m(archivo_inicial, archivo_7_matrices, diccionario_fuego)

    # --- 2. EJECUTAR SIMULACIÓN DE AVANCE (fire2) ---
    print("\n=== PASO 2: Simulación de Avance del Fuego ===")
    # Nota: fire2 pedirá por consola las coordenadas X e Y de inicio
    fire2.avance_fuego(archivo_7_matrices, archivo_evolucion, velocidad_viento,  viento_x, viento_y)

    # --- 3. GENERAR VIDEO DE LA SIMULACIÓN (mapa) ---
    print("\n=== PASO 3: Generando Video ===")
    # wx, wy son la dirección del viento para la flecha visual
 
    mapa.generar_video_incendio(archivo_evolucion, archivo_video, viento_x, viento_y)

    print("\n==============================================")
    print(f"PROCESO FINALIZADO CON ÉXITO")
    print(f"Video disponible en: {archivo_video}.mp4")
    print("==============================================")

if __name__ == "__main__":
    main()