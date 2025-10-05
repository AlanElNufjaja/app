import numpy as np

g = 9.81  # m/s²
DENSIDAD_ROCA = 2700
DENSIDAD_BLANDA = 1800
DENSIDAD_AGUA = 1000

def calcular_impacto(radio_ast, velocidad_ms, densidad_ast, material):
    """
    Calcula energía y características del cráter según el material de impacto.

    Parámetros:
        radio_ast: radio del meteorito (m)
        velocidad_ms: velocidad del meteorito (m/s)
        densidad_ast: densidad del meteorito (kg/m³)
        material: "Roca dura", "Tierra blanda" o "Agua"

    Retorna:
        dict con:
            masa, energia_joules, energia_megatones,
            diametro_m, profundidad_m, radio_km
    """
    # ----- Masa y energía -----
    volumen = (4/3) * np.pi * (radio_ast**3)
    masa = densidad_ast * volumen
    energia_joules = 0.5 * masa * velocidad_ms**2
    energia_megatones = energia_joules / 4.184e15

    # ----- Cráter según material -----
    ESCALA_IMPACTO = 1.0 / 1000  # metros -> km para el mapa

    if material == "Roca dura":
        K = 0.1
        diametro_m = K * (energia_joules / (DENSIDAD_ROCA * g))**0.25
        profundidad_m = diametro_m / 5
        radio_km = max(diametro_m / 2 * ESCALA_IMPACTO, 0.05)
    elif material == "Tierra blanda":
        K = 0.1
        diam_roca = K * (energia_joules / (DENSIDAD_ROCA * g))**0.25
        prof_roca = diam_roca / 5
        diametro_m = diam_roca * 1.15
        profundidad_m = prof_roca * 0.70
        radio_km = max(diametro_m / 2 * ESCALA_IMPACTO, 0.05)
    else:  # Agua
        C = 0.1
        radio_desplazamiento = C * (energia_joules / (DENSIDAD_AGUA * g))**(1/3)
        altura_inicial_m = radio_desplazamiento * 2 / radio_ast
        diametro_m = altura_inicial_m  # usamos como diámetro visible
        profundidad_m = altura_inicial_m  # no hay cráter real
        radio_km = max(altura_inicial_m * ESCALA_IMPACTO * 2, 0.05)

    return {
        "masa": masa,
        "energia_joules": energia_joules,
        "energia_megatones": energia_megatones,
        "diametro_m": diametro_m,
        "profundidad_m": profundidad_m,
        "radio_km": radio_km
    }
