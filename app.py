import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, velocidad_realista, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa
from red import perdida_tamano_meteorito  # 🔹 importamos la función externa

st.title("Visualizador de Meteoritos 2D ☄️")

# ======================
# Cargar datos
# ======================
datos_base = pd.read_csv("datos_base.csv")
datos_limpios = pd.read_csv("datos_limpios.csv")

# Combinar datos para acceder a tamaño y velocidad
meteoritos = pd.concat([datos_base, datos_limpios], axis=1)
opciones = meteoritos['id'].astype(str).tolist()
meteorito_seleccionado = st.sidebar.selectbox("Selecciona un meteorito", opciones)

mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# ======================
# Datos predeterminados del meteorito
# ======================
tamano_inicial = (
    (mete['estimated_diameter.kilometers.estimated_diameter_min'] +
     mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2
) * 1000  # km → m

densidad = 3000  # kg/m³ estándar
velocidad_kms = mete['relative_velocity.kilometers_per_second']  # valor base en km/s

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Longitud manual", float(-180), float(180), -99.1, step=0.0001)

# 🔹 Sliders con valores iniciales tomados del CSV
tamano_inicial = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500.0, float(tamano_inicial))
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, int(densidad))

# 🔹 NUEVO: slider para ajustar velocidad basada en la del CSV
velocidad_kms = st.sidebar.slider(
    "Velocidad de entrada (km/s)",
    5.0, 80.0, float(velocidad_kms), step=0.1
)

# 🔹 Ajuste opcional del factor de abrasión atmosférica
exp_factor = st.sidebar.slider(
    "Nivel de abrasión atmosférica (potencia de 10)",
    -9.0, -6.0, -7.0, step=0.1
)
factor_calor = (10 ** exp_factor) * 100
st.sidebar.write(f"Constante actual: {factor_calor:.1e}")

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Convertir velocidad de km/s a m/s
velocidad_ms = velocidad_kms * 1000

# Calcular tamaño final (usando el valor ajustado de abrasión)
tamano_final = perdida_tamano_meteorito(densidad, velocidad_ms, tamano_inicial, factor_calor)

# Calcular radio de impacto con tamaño reducido
radio_km = calcular_radio_impacto(tamano_final, densidad, velocidad_kms)

# Generar puntos de impacto
df = generar_puntos_circulo(lat, lon, radio_km)

# ======================
# Mostrar resultados
# ======================
st.subheader("🔍 Resultados de la simulación")

st.write(f"**Tamaño inicial:** {tamano_inicial:.2f} m")
st.write(f"**Tamaño final tras entrar a la atmósfera:** {tamano_final:.2f} m")
st.write(f"**Densidad:** {densidad} kg/m³")
st.write(f"**Velocidad de entrada:** {velocidad_kms:.2f} km/s")
st.write(f"**Radio estimado de impacto:** {radio_km:.2f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# ======================
# Mostrar mapa
# ======================
mostrar_mapa(df, lat, lon, radio_km)
