import streamlit as st
import pandas as pd
import numpy as np
from parameters import obtener_coordenadas, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa
from red import perdida_tamano_meteorito  
from PIL import Image

# Carga la imagen
img = Image.open("Logo1.png")

# Muestra la imagen con un ancho específico
col1, col2, col3 = st.columns([1,3,2])
with col2:
    st.image(img, use_container_width=True)

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
meteorito_seleccionado = st.sidebar.selectbox("Select a meteorite", opciones)
mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# ======================
# Datos predeterminados del meteorito
# ======================
tamano_inicial = (
    (mete['estimated_diameter.kilometers.estimated_diameter_min'] +
     mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2
)  

velocidad_kms = mete['relative_velocity.kilometers_per_second']  

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("City name")
lat_manual = st.sidebar.slider("Manual latitude", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Manual longitude", float(-180), float(180), -99.1, step=0.0001)

tamano_inicial = st.sidebar.slider("Meteorite size (km)", 0.0, 10.0, float(tamano_inicial), 0.0001)
densidad = st.sidebar.slider("Density (kg/m³)", 1000, 8000, 3000)
velocidad_kms = st.sidebar.slider("Velocity (km/s)", 1.0, 30.0, float(velocidad_kms), 0.1)
material = st.sidebar.selectbox(
    "Select impact material",
    ["Hard rock", "Soft soil", "Water"])
tipodano = st.sidebar.selectbox(
    "Type of damage",
    ["Impact and crater", "Fireball", "Sound","Earthquakes"])
factor_calor = (2.3e-2)  
st.sidebar.write(f"Heat constant: {factor_calor:.1e}")

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

tamano_final = perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor)

radio_km = calcular_radio_impacto(tamano_final, densidad, velocidad_kms)
radio_km = max(radio_km, 0.0)  

energia = (0.5 * densidad * (4/3 * np.pi * (radio_km*10)**3) * (velocidad_kms*10)**2) / 4.184e+13


if material == "Hard rock":
    profundidad_m = radio_km*2 / 5

elif material == "Soft soil":
    radio_km = max(radio_km * 1.15, 0.0)
    profundidad_m = (radio_km*2 / 5)* 1/7

else:  
    radio_km = max(tamano_inicial * 1/50, 0.0)
    profundidad_m = (0)
        
df = generar_puntos_circulo(lat, lon, radio_km)

radio_km /= 50
# ======================
# Mostrar resultados
# ======================
col0, col1, col2 = st.columns([1, 2, 1])
with col1:
    st.subheader("Simulation results")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Initial size:** {tamano_inicial:.6f} km")
    st.write(f"**Density:** {densidad} kg/m³")
    st.write(f"**Impact velocity:** {velocidad_kms:.2f} km/s")
    st.write(f"**Impact energy:** {energia:.3f} MT")

with col2:
    st.write(f"**Final size after atmospheric entry:** {tamano_final:.6f} km")
    st.write(f"**Crater radius:** {radio_km:.3f} km")
    st.write(f"**Impact depth:** {profundidad_m:.3f} km")
    st.write(f"**Coordinates:** {lat:.4f}, {lon:.4f}")

mostrar_mapa(df, lat, lon, radio_km,tipodano)
