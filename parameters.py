# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(lugar="", manual_lat=0.0, manual_lon=0.0):
    """
    Obtiene coordenadas usando geopy si hay nombre de lugar.
    Si falla o no hay lugar, usa lat/lon manual.
    Si tampoco hay, devuelve Ciudad de México.
    """
    if lugar:
        try:
            geolocator = Nominatim(user_agent="meteor_app")
            location = geolocator.geocode(lugar, timeout=10)
            if location:
                return location.latitude, location.longitude
        except:
            pass
    
    # Usa lat/lon manual si están proporcionadas
    if manual_lat != 0.0 or manual_lon != 0.0:
        return manual_lat, manual_lon
    
    # fallback por defecto
    return 19.4326, -99.1332

def calcular_radio(tamano):
    """Calcula radio de impacto en km según tamaño del meteorito"""
    return tamano * 0.1
