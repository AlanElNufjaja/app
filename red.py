def perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor):
    velocidad_ms = velocidad_kms * 1000
    energia = 0.5 * densidad * (velocidad_kms**2)

    # Pérdida proporcional a la energía y al factor_calor
    perdida_tamano = factor_calor * energia / densidad

    # Aumentar la pérdida si el meteorito es muy pequeño o va muy rápido
    if tamano_inicial < 1:  # Umbral para meteoritos pequeños
        perdida_tamano *= 2
    if velocidad_kms > 20:  # Umbral para velocidades altas
        perdida_tamano *= 1.5

    # Limitar pérdida máxima relativa al tamaño
    perdida_tamano = min(perdida_tamano, tamano_inicial)  # Desintegración total si la pérdida es mayor que el tamaño

    # Tamaño final
    if perdida_tamano >= tamano_inicial:
        tamano_final = 0  # Desintegración total
    else:
        tamano_final = tamano_inicial - perdida_tamano

    return tamano_final
