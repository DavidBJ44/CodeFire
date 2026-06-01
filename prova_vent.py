
sigma = 1770
beta = 0.03969
velocidad_viento = 10  # km/h
alpha = 0
import math

C = 7.47 * math.exp(-0.133 * (sigma ** 0.55 ))
B = 0.02526 * (sigma ** 0.54)
E = 0.715 * math.exp(-0.000359 * sigma)
beta_opt = 3.348 * (sigma ** -0.8189)
U = velocidad_viento * 54.68 # Convertir de km/h a ft/min
U_efectivo = U * math.cos(alpha)  # Componente del viento en la dirección del fuego
phi_v = C * (U_efectivo**B) * ((beta/beta_opt) ** (-E)) 
print(phi_v)