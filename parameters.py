# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(lugar, manual_lat=0.0, manual_lon=0.0):
    """
    Obtiene coordenadas usando geopy.
    Si no se encuentra o hay error, usa coordenadas manuales o Ciudad de México por defecto.
    """
    if lugar:
        try:
            geolocator = Nominatim(user_agent="meteor_app")
            location = geolocator.geocode(lugar)
            if location:
                return location.latitude, location.longitude
        except:
            pass

    # Si falla, usa coordenadas manuales
    if manual_lat != 0.0 or manual_lon != 0.0:
        return manual_lat, manual_lon

    # fallback por defecto
    return 19.4326, -99.1332

def calcular_radio(tamano):
    """Calcula radio de impacto en km según tamaño del meteorito"""
    return tamano * 0.1
