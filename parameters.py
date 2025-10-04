# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(nombre_ciudad, lat_manual=0.0, lon_manual=0.0):
    """
    Convierte un nombre de ciudad a latitud y longitud usando Geopy.
    Si no se encuentra la ciudad o hay un error, retorna las coordenadas manuales.
    
    nombre_ciudad: str - nombre de la ciudad que el usuario ingresa
    lat_manual: float - latitud manual por defecto
    lon_manual: float - longitud manual por defecto
    """
    # Si no se escribe ciudad, usar coordenadas manuales
    if nombre_ciudad.strip() == "":
        return lat_manual, lon_manual

    try:
        geolocator = Nominatim(user_agent="meteoro_app")
        location = geolocator.geocode(nombre_ciudad, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            # Si no encuentra la ciudad, usar coordenadas manuales
            return lat_manual, lon_manual
    except:
        # Si hay error de conexión o cualquier excepción, fallback
        return lat_manual, lon_manual


def calcular_radio(tamano_metro):
    """
    Calcula un radio estimado de impacto en kilómetros según el tamaño del meteorito.
    Esto es un ejemplo simple: cuanto más grande, más radio de impacto.
    
    tamano_metro: float - tamaño del meteorito en metros
    """
    # Simple proporcional: 1 metro = 0.1 km de radio
    radio_km = tamano_metro * 0.1
    return radio_km
