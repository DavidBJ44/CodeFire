# Simulador d'Incendis Forestals

Aquest programari simula la propagació d'un incendi forestal.

## Requisits

- Python 3.x
- Llibreries: numpy, pandas, matplotlib
- Programari extern: FFmpeg (necessari per a l'exportació de vídeo)

## Estructura de mòduls

- mainfire.py: Punt d'entrada i coordinació del sistema.
- fire2.py: Càlcul de la propagació cel·la a cel·la (pendent i vent).
- F_RP.py: Transformació de models de sòl en matrius d'energia (Ea i Pq).
- ffmc.py / bui.py: Càlcul d'índexs d'humitat del combustible (FWI).
- mapa.py: Generació del vídeo MP4 a partir dels resultats.

## Instruccions d'ús

1. Preparació de dades:
   - Col·locar els històrics meteorològics a la carpeta `csv/`.
   - Definir el terreny i l'altitud al fitxer `matrices_solo.txt`.

2. Execució:
   python mainfire.py