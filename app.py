import streamlit as st
from parameters import obtener_coordenadas
from damage import generar_puntos_circulo, calcular_radio_impacto
from mapa import mostrar_mapa
import streamlit as st
from asteroides import lista_ids, datos_meteorito

# Selección del meteorito
meteorito_seleccionado = st.selectbox("Selecciona un meteorito", lista_ids())

# Obtener datos
datos = datos_meteorito(meteorito_seleccionado)
if datos:
    st.write(datos)
    # Aquí puedes usar datos['relative_velocity.kilometers_per_second'], datos['estimated_diameter.kilometers.estimated_diameter_max'], etc.

st.set_page_config(layout="wide")
st.title("Visualizador de Meteoritos 2D ☄️")

# -------------------------
# Panel lateral: entrada del usuario
# -------------------------
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", -80, 80, 19)
lon_manual = st.sidebar.slider("Longitud manual", -180, 180, -99)

tamano = st.sidebar.slider("Diámetro del meteorito (m)", 10, 15000, 100)
densidad = st.sidebar.slider("Densidad (kg/m³)", 100, 10_000, 3000)
velocidadkms = st.sidebar.slider("Velocidad (km/s)", 1, 30, 5)

# -------------------------
# Obtener coordenadas
# -------------------------
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# -------------------------
# Calcular radio y puntos
# -------------------------
radio_km = calcular_radio_impacto(tamano, densidad, velocidadkms)
df = generar_puntos_circulo(lat, lon, radio_km)

# -------------------------
# Mostrar info
# -------------------------
st.write(f"Coordenadas: {lat:.4f}, {lon:.4f}")
st.write(f"Diámetro: {tamano} m | Densidad: {densidad} kg/m³ | Velocidad: {velocidadkms} km/s")
st.write(f"Radio estimado de impacto: {radio_km:.2f} km")

# -------------------------
# Mostrar mapa
# -------------------------
mostrar_mapa(df, lat, lon, radio_km)
