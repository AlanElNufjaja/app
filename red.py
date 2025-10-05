def perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor):
    velocidad_ms = velocidad_kms * 1000
    energia = 0.5 * densidad * (velocidad_kms**2)

    # Pérdida proporcional a la energía y al factor_calor
    perdida_tamano = factor_calor * energia / densidad

    # Limitar pérdida máxima relativa al tamaño
    perdida_tamano = min(perdida_tamano, 0.95 * tamano_inicial)

    # Tamaño final mínimo para no desaparecer
    tamano_final = max(tamano_inicial - perdida_tamano, 0.1)

    return tamano_final

