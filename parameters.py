# parameters.py
from geopy.geocoders import Nominatim

def obtener_coordenadas(nombre_ciudad, lat_manual=0.0, lon_manual=0.0):
    """
    Convierte un nombre de ciudad a lat/lon usando Geopy.
    Si no se encuentra o hay error, usa lat/lon manual.
    """
    if nombre_ciudad.strip() == "":
        return normalizar_coordenadas(lat_manual, lon_manual)

    try:
        geolocator = Nominatim(user_agent="meteoro_app")
        location = geolocator.geocode(nombre_ciudad, timeout=10)
        if location:
            return normalizar_coordenadas(location.latitude, location.longitude)
        else:
            return normalizar_coordenadas(lat_manual, lon_manual)
    except:
        return normalizar_coordenadas(lat_manual, lon_manual)


def normalizar_coordenadas(lat, lon):
    """
    Normaliza latitud (-90 a 90) y longitud (-180 a 180)
    Incluso si se pasan valores enormes.
    """
    # Normalizar longitud
    lon = ((lon + 180) % 360) - 180

    # Normalizar latitud
    # La latitud “rebota” en los polos
    while lat > 90 or lat < -90:
        if lat > 90:
            lat = 180 - lat
            lon += 180  # giro de hemisferio
        elif lat < -90:
            lat = -180 - lat
            lon += 180
        # normalizamos lon después de cada cambio
        lon = ((lon + 180) % 360) - 180

    return lat, lon


def calcular_radio(tamano_metro):
    """
    Calcula un radio estimado de impacto en km según tamaño del meteorito.
    """
    radio_km = tamano_metro * 0.1
    return radio_km
