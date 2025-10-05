import numpy as np

G = 6.674e-11  # Constante Gravitacional (No se usa directamente aquí, solo para referencia)
g = 9.81       # Aceleración de la gravedad (m/s^2)
DENSIDAD_ASTEROIDE = 3000  # Densidad típica de asteroide rocoso (kg/m^3)
DENSIDAD_ROCA = 2700       # Densidad de la corteza (kg/m^3)
DENSIDAD_BLANDA = 1800     # Densidad de suelo blando/sedimento (kg/m^3)
DENSIDAD_AGUA = 1000       # Densidad del agua (kg/m^3)
radio_ast = 50.0  # Radio del asteroide (m). Diámetro total = 100m.
vel_impacto = 20000.0  # Velocidad de impacto típica (m/s), o 20 km/s.
def calcular_energia(radio, velocidad, densidad_ast):
    """Calcula la masa y la energía cinética del asteroide."""
    volumen = (4/3) * np.pi * (radio**3)
    masa = densidad_ast * volumen
    # E_k = 0.5 * m * v^2
    energia_joules = 0.5 * masa * (velocidad**2)
    # Convertir a Megatones de TNT para mejor comprensión (1 Mt = 4.184e15 J)
    energia_megatones = energia_joules / 4.184e15
    return masa, energia_joules, energia_megatones

masa_ast, ek_joules, ek_megatones = calcular_energia(radio_ast, vel_impacto, DENSIDAD_ASTEROIDE)

def impacto_roca_dura(ek):
    """Estima el diámetro del cráter en roca dura."""
    # K ~ 0.1, usando la fórmula de escalamiento
    K = 0.1
    # La fórmula es D_crater = K * (E_k / (rho * g))^(1/4)
    denominador = DENSIDAD_ROCA * g
    diametro_m = K * (ek / denominador)**(1/4)
    # Profundidad típica es ~1/5 del diámetro
    profundidad_m = diametro_m / 5
    return diametro_m, profundidad_m

def impacto_tierra_blanda(diam_roca, prof_roca):
    """Estima el cráter en tierra blanda/sedimentos (escalado empíricamente)."""
    # Se asume un cráter 15% más ancho y 30% menos profundo que en roca
    diam_blanda = diam_roca * 1.15
    prof_blanda = prof_roca * 0.70
    return diam_blanda, prof_blanda

def impacto_agua(ek, radio_ast):
    """Estima la altura inicial de la columna de agua (H) en el punto de impacto."""
    # Fórmula: H_agua ~ C * (E_k / (rho * g))^(1/3) * (1/R)
    C = 0.1
    denominador = DENSIDAD_AGUA * g
    # Calcular radio del hemisferio de agua desplazada (similar al "radio del cráter" virtual)
    radio_desplazamiento = C * (ek / denominador)**(1/3)
    altura_inicial_m = radio_desplazamiento * 2 / radio_ast  # Factor de escalamiento simple
    return altura_inicial_m

diam_roca, prof_roca = impacto_roca_dura(ek_joules)
diam_blanda, prof_blanda = impacto_tierra_blanda(diam_roca, prof_roca)
alt_agua_inicial = impacto_agua(ek_joules, radio_ast)
