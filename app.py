import streamlit as st
from damage import generar_puntos_circulo, calcular_radio_impacto
from mapa import mostrar_mapa
from asteroides import cargar_meteoritos, lista_ids, datos_meteorito

# -----------------------
# Cargar datos y seleccionar meteorito
# -----------------------
df_meteoritos = cargar_meteoritos()
meteorito_id = st.sidebar.selectbox("Selecciona un meteorito", lista_ids(df_meteoritos))
datos = datos_meteorito(df_meteoritos, meteorito_id)

# -----------------------
# Mostrar y permitir modificar parámetros
# -----------------------
if datos:
    st.sidebar.markdown("### Parámetros del meteorito")
    tamano_default = float(datos['estimated_diameter.kilometers.estimated_diameter_max'] * 1000)
    velocidad_default = float(datos['relative_velocity.kilometers_per_second'])
    densidad_default = 3000  # valor aproximado por defecto

    tamano = st.sidebar.slider("Tamaño del meteorito (m)", 10, 5000, int(tamano_default))
    velocidadkms = st.sidebar.slider("Velocidad (km/s)", 5.0, 80.0, float(velocidad_default), step=0.1)
    st.write("La densidad mas comun es 200kg/m³)
    densidad = st.sidebar.slider("Densidad (kg/m³)", 100, 10000, 200)

    # Coordenadas manuales
    lat_manual = st.sidebar.slider("Latitud", -90, 90, 19)
    lon_manual = st.sidebar.slider("Longitud", -180, 180, -99)

    # Calcular radio
    radio_km = calcular_radio_impacto(tamano, densidad, velocidadkms)

    # Generar puntos del círculo
    df_circulo = generar_puntos_circulo(lat_manual, lon_manual, radio_km)

    # Mostrar info
    st.write(f"ID: {meteorito_id}")
    st.write(f"Tamaño: {tamano} m, Velocidad: {velocidadkms} km/s, Densidad: {densidad} kg/m³")
    st.write(f"Radio de impacto estimado: {radio_km:.2f} km")
    st.write(f"Coordenadas: {lat_manual}, {lon_manual}")

    # Mostrar mapa
    mostrar_mapa(df_circulo, lat_manual, lon_manual, radio_km)
else:
    st.error("No se encontró el meteorito seleccionado.")
