# parameters.py

def obtener_coordenadas(lugar):
    """
    Obtiene coordenadas según el nombre del lugar.
    Si no hay lugar o no se encuentra, devuelve Ciudad de México.
    """
    lugares_simulados = {
        "mexico": (19.4326, -99.1332),
        "tokyo": (35.6895, 139.6917),
        "paris": (48.8566, 2.3522)
    }
    
    if lugar:
        key = lugar.lower()
        if key in lugares_simulados:
            return lugares_simulados[key]
    
    # Si no hay lugar válido, Ciudad de México por defecto
    return 19.4326, -99.1332

def calcular_radio(tamano):
    """Calcula radio de impacto en km según tamaño del meteorito"""
    return tamano * 0.1
