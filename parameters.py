# parameters.py
from geopy.geocoders import Nominatim

# Límites
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

# Velocidades típicas (km/s)
VEL_MIN, VEL_MAX = 11, 72

def obtener_coordenadas(nombre_ciudad, lat_manual=19.4326, lon_manual=-99.1332):
    """
    Convierte un nombre de ciudad a lat/lon usando Geopy.
    Si falla o está vacío, usa lat/lon manual y ajusta a límites válidos.
    """
    # Aplicar límites inmediatamente a los parámetros manuales
    lat_manual = max(LAT_MIN, min(LAT_MAX, lat_manual))
    lon_manual = max(LON_MIN, min(LON_MAX, lon_manual))

    # Siempre partimos de las coordenadas manuales como fallback
    lat, lon = lat_manual, lon_manual

    if nombre_ciudad.strip() != "":
        try:
            geolocator = Nominatim(user_agent="meteoro_app")
            location = geolocator.geocode(nombre_ciudad, timeout=5)  # timeout corto
            if location:
                lat, lon = location.latitude, location.longitude
        except:
            pass  # si falla, usamos lat/lon manual

    # Aplicar límites de nuevo después de usar geopy
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    lon = max(LON_MIN, min(LON_MAX, lon))
    return lat, lon


def velocidad_realista(tamano_m):
    """
    Calcula la velocidad promedio de impacto según tamaño del meteorito.
    Los meteoritos pequeños se frenan mucho y se desintegran, los grandes mantienen velocidad.
    tamano_m: diámetro en metros
    Retorna velocidad en km/s
    """
    if tamano_m < 1:
        return 0  # se desintegra
    elif tamano_m < 10:
        return 12  # pequeños, frenados
    elif tamano_m < 50:
        return 20  # medianos
    else:
        return 25  # grandes

def calcular_radio_impacto(tamano_m, densidad, velocidad_kms, k=0.05):
    """
    Calcula un radio estimado de destrucción en km según parámetros del meteorito:
    - tamano_m: diámetro en metros
    - densidad: kg/m³
    - velocidad_kms: velocidad en km/s
    """
    velocidad = velocidad_kms * 1000  # pasar a m/s
    radio = k * (tamano_m**(1/3)) * (densidad**(1/3)) * (velocidad**(2/3))
    return radio
