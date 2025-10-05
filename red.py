def perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor):
    """
    Calcula la pérdida aproximada de tamaño de un meteorito al entrar en la atmósfera.
    Parámetros:
      densidad: densidad del meteorito (kg/m³)
      velocidad: velocidad de entrada (m/s)
      tamano_inicial: diámetro inicial del meteorito (m)
    Retorna:
      tamaño final estimado (m)
    """
    # --- Parámetros de simulación simplificados ---
    coef_resistencia = 0.47        # coeficiente de arrastre (esfera)
    densidad_aire = 1.225           # kg/m³ al nivel del mar
  
    # Energía cinética por unidad de volumen (simplificada)
    energia = 0.5 * densidad * (velocidad_kms**2)
    
    # Pérdida estimada de masa (proporcional a energía y área)
    area = 3.1416 * (tamano_inicial / 2)**2
    perdida_tamano = factor_calor * energia * area / densidad
    
    # Evita valores negativos
    tamano_final = max(tamano_inicial - perdida_tamano, 0)
    
    return tamano_final
