import streamlit as st
import pandas as pd
import numpy as np
from parameters import obtener_coordenadas, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa
from red import perdida_tamano_meteorito  # 🔹 función adaptada a km

st.title("Visualizador de Meteoritos ☄️")

g = 9.81  # m/s²
DENSIDAD_ROCA = 2700
DENSIDAD_BLANDA = 1800
DENSIDAD_AGUA = 1000
ESCALA_IMPACTO = 1.0 / 1000
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
)  # ahora en km

velocidad_kms = mete['relative_velocity.kilometers_per_second']  # km/s

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Longitud manual", float(-180), float(180), -99.1, step=0.0001)

tamano_inicial = st.sidebar.slider("Tamaño del meteorito (km)", 0.0, 10.0, float(tamano_inicial), 0.0001)
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, 3000)
velocidad_kms = st.sidebar.slider("Velocidad (km/s)", 1.0, 30.0, float(velocidad_kms), 0.1)
material = st.sidebar.selectbox(
    "Selecciona el material del impacto",
    ["Roca dura", "Tierra Blanda", "Agua"])
# 🔹 Ajuste opcional del factor de abrasión atmosférica
exp_factor = st.sidebar.slider(
    "Nivel de abrasión atmosférica (potencia de 10)",
    -9.0, -7.5, -9.0, step=0.01
)
factor_calor = (10 ** exp_factor)*0.1  # ajustado para km
st.sidebar.write(f"Constante actual: {factor_calor:.1e}")

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Calcular tamaño final (usando el valor ajustado de abrasión)
tamano_final = perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor)
tamano_final = max(tamano_final, 0.000)  # evitar tamaños negativos

# Calcular radio de impacto con tamaño reducido (ahora todo en km)
radio_km = calcular_radio_impacto(tamano_final, densidad, velocidad_kms)
radio_km = max(radio_km, 0.0)  # asegurar visibilidad en el mapa

energia_joules = 0.5 * densidad * (4/3 * np.pi * radio_km**3) * velocidad_kms**2

if material == "Roca dura":
    profundidad_m = radio_km*2 / 5

elif material == "Tierra blanda":
    radio_km = max(tamano_inicial * 1.15, 0.0)
    profundidad_m = (radio_km*2 / 5)* 1/7

else:  # Agua
    radio_km = max(tamano_inicial * 1/50, 0.0)
    profundidad_m = (0)
        
# Generar puntos de impacto
df = generar_puntos_circulo(lat, lon, radio_km)

# ======================
# Mostrar resultados
# ======================
st.subheader("🔍 Resultados de la simulación")
st.write(f"**Tamaño inicial:** {tamano_inicial:.6f} km")
st.write(f"**Tamaño final tras entrar a la atmósfera:** {tamano_final:.6f} km")
st.write(f"**Densidad:** {densidad} kg/m³")
st.write(f"**Velocidad de impacto:** {velocidad_kms:.2f} km/s")
st.write(f"**Radio estimado de impacto:** {radio_km:.3f} km")
st.write(f"**Profundidad de impacto:** {profundidad_m:.3f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# ======================
# Mostrar mapa
# ======================
mostrar_mapa(df, lat, lon, radio_km)
