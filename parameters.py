# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(lugar="", manual_lat=0.0, manual_lon=0.0):
    """
    Devuelve lat/lon de un lugar con geopy.
    Si geopy falla o no hay lugar, usa lat/lon manual.
    Si tampoco hay, usa Ciudad de México por defecto.
    """
    if lugar:
        try:
            geolocator = Nominatim(user_agent="meteor_app")
            location = geolocator.geocode(lugar, timeout=10)
            if location:
                return location.latitude, location.longitude
        except:
            pass  # falla geopy, sigue al fallback

    # Lat/lon manual
    if manual_lat != 0.0 or manual_lon != 0.0:
        return manual_lat, manual_lon

    # Fallback por defecto
    return 19.4326, -99.1332

def calcular_radio(tamano):
    """Calcula radio de impacto en km según tamaño del meteorito"""
    return tamano * 0.1
