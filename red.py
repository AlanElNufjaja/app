def perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor):
    velocidad_ms = velocidad_kms * 1000
    energia = 0.5 * densidad * (velocidad_ms**2)

    # Pérdida proporcional a la energía y al factor_calor
    perdida_tamano = factor_calor * energia / densidad

    # Aumentar la pérdida si el meteorito es muy pequeño, va muy rápido o tiene baja densidad
    if tamano_inicial < 1 and velocidad_kms > 0.5:  # Umbral para meteoritos pequeños y veloces
        perdida_tamano *= 2
    if densidad < 2000 and velocidad_kms > 0.5:  # Umbral para meteoritos de baja densidad y veloces
        perdida_tamano *= 1.5
    if velocidad_kms > 10:  # Umbral para velocidades muy altas
        perdida_tamano *= 1.2

    # Limitar pérdida máxima relativa al tamaño
    perdida_tamano = min(perdida_tamano, tamano_inicial)  # Desintegración total si la pérdida es mayor que el tamaño

    # Tamaño final
    if perdida_tamano >= tamano_inicial and tamano_inicial < 5:  # Solo se desintegra si el tamaño es pequeño
        tamano_final = 0  # Desintegración total
    else:
        tamano_final = tamano_inicial - perdida_tamano
        if tamano_final < 0.1:  # Umbral mínimo para considerar que el meteorito se ha desintegrado
            tamano_final = 0

    return tamano_final
