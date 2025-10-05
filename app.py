import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, velocidad_realista, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa
from red import perdida_tamano_meteorito

st.title("Visualizador de Meteoritos 2D ☄️")

# ======================
# Cargar datos
# ======================
try:
    datos_base = pd.read_csv("datos_base.csv")
    datos_limpios = pd.read_csv("datos_limpios.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontraron los archivos CSV 'datos_base.csv' o 'datos_limpios.csv'.")
    st.stop()

# 🔹 Verificación básica
st.sidebar.write("Datos cargados:", len(datos_base), "meteoritos")

# Combinar datos por columnas
meteoritos = pd.concat([datos_base.reset_index(drop=True), datos_limpios.reset_index(drop=True)], axis=1)

# Asegurar columna 'id' disponible
if 'id' not in meteoritos.columns:
    st.error("❌ No se encontró la columna 'id' en los datos.")
    st.write("Columnas disponibles:", meteoritos.columns.tolist())
    st.stop()

# ======================
# Selección de meteorito
# ======================
opciones = meteoritos['id'].astype(str).unique().tolist()
meteorito_seleccionado = st.sidebar.selectbox("Selecciona un meteorito", opciones)

# Verificar que se encontró correctamente
if meteorito_seleccionado not in opciones:
    st.warning("⚠️ Meteorito no encontrado en los datos.")
    st.stop()

mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# ======================
# Datos base del meteorito
# ======================
try:
    tamano_inicial = (
        (mete['estimated_diameter.kilometers.estimated_diameter_min'] +
         mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2
    ) * 1000  # km → m
except KeyError:
    st.error("❌ No se encontraron las columnas de diámetro estimado.")
    st.write("Columnas disponibles:", meteoritos.columns.tolist())
    st.stop()

try:
    velocidad_kms = float(mete['relative_velocity.kilometers_per_second'])
except KeyError:
    st.error("❌ No se encontró la columna de velocidad.")
    st.stop()

densidad = 3000  # valor estándar

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Longitud manual", float(-180), float(180), -99.1, step=0.0001)

# Sliders configurables
tamano_inicial = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500.0, float(tamano_inicial))
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, int(densidad))
velocidad_kms = st.sidebar.slider("Velocidad de entrada (km/s)", 5.0, 80.0, float(velocidad_kms), step=0.1)

# Factor atmosférico
exp_factor = st.sidebar.slider("Nivel de abrasión atmosférica (potencia de 10)", -9.0, -6.0, -7.0, step=0.1)
factor_calor = (10 ** exp_factor) * 100
st.sidebar.write(f"Constante actual: {factor_calor:.1e}")

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

if lat is None or lon is None:
    st.error("❌ No se pudieron obtener coordenadas válidas.")
    st.stop()

velocidad_ms = velocidad_kms * 1000
tamano_final = perdida_tamano_meteorito(densidad, velocidad_ms, tamano_inicial, factor_calor)
radio_km = calcular_radio_impacto(tamano_final, densidad, velocidad_kms)

if radio_km <= 0 or pd.isna(radio_km):
    st.warning("⚠️ Radio de impacto no válido. Verifica los parámetros.")
    st.stop()

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
st.subheader("🗺️ Mapa de impacto")
mostrar_mapa(df, lat, lon, radio_km)
