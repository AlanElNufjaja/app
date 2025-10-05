def perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor):
    """
    Calcula la pérdida aproximada de tamaño de un meteorito al entrar en la atmósfera.
    Parámetros:
      densidad: densidad del meteorito (kg/m³)
      velocidad_kms: velocidad de entrada (km/s)
      tamano_inicial: diámetro inicial del meteorito (m)
      factor_calor: factor ajustable de abrasión
    Retorna:
      tamaño final estimado (m)
    """
    # --- Parámetros simplificados ---
    velocidad_ms = velocidad_kms * 1000  # convertir km/s a m/s
    energia = 0.5 * densidad * (velocidad_ms**2)  # energía cinética por unidad de volumen

    # Pérdida proporcional a la energía por unidad de masa
    perdida_tamano = factor_calor * energia / densidad

    # Limitar pérdida máxima
    perdida_tamano = min(perdida_tamano, 0.9 * tamano_inicial)

    # Calcular tamaño final
    tamano_final = max(tamano_inicial - perdida_tamano, 0.1)

    return tamano_final
