# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(nombre_ciudad, lat_manual=0.0, lon_manual=0.0):
    """
    Convierte nombre de ciudad a lat/lon usando Geopy.
    Si falla o está vacío, retorna las coordenadas manuales.
    """
    if nombre_ciudad.strip() == "":
        return lat_manual, lon_manual

    try:
        geolocator = Nominatim(user_agent="meteoro_app")
        location = geolocator.geocode(nombre_ciudad, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return lat_manual, lon_manual
    except:
        return lat_manual, lon_manual
