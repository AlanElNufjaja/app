import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas
from damage import generar_puntos_circulo
from mapa import mostrar_mapa
from red import perdida_tamano_meteorito

from calculos import calcular_energia, impacto_roca_dura, impacto_tierra_blanda, impacto_agua

st.title("Visualizador de Meteoritos 2D ☄️")

# ======================
# Cargar datos
# ======================
datos_base = pd.read_csv("datos_base.csv")
datos_limpios = pd.read_csv("datos_limpios.csv")

meteoritos = pd.concat([datos_base, datos_limpios], axis=1)
opciones = meteoritos['id'].astype(str).tolist()
meteorito_seleccionado = st.sidebar.selectbox("Selecciona un meteorito", opciones)
mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# ======================
# Datos base del meteorito
# ======================
tamano_inicial = (
    (mete['estimated_diameter.kilometers.estimated_diameter_min'] +
     mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2
) * 1000  # km → m

densidad = 3000
velocidad_kms = mete['relative_velocity.kilometers_per_second']

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", -80.0, 80.0, 19.44, 0.0001)
lon_manual = st.sidebar.slider("Longitud manual", -180.0, 180.0, -99.1, 0.0001)

tamano_inicial = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500.0, float(tamano_inicial))
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, int(densidad))
velocidad_kms = st.sidebar.slider("Velocidad (km/s)", 1.0, 30.0, float(velocidad_kms), 0.1)

exp_factor = st.sidebar.slider("Nivel de abrasión atmosférica (potencia de 10)", -9.0, -6.0, -7.0, 0.1)
factor_calor = 10 ** exp_factor * 1e-4
st.sidebar.write(f"Constante actual: {factor_calor:.1e}")

material = st.sidebar.selectbox("Superficie de impacto", ["Roca dura", "Tierra blanda", "Agua"])

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)
velocidad_ms = velocidad_kms * 1000

# Pérdida de tamaño
tamano_final = perdida_tamano_meteorito(densidad, velocidad_kms, tamano_inicial, factor_calor)

# Calcular energía del meteorito
masa, ek_joules, ek_megatones = calcular_energia(tamano_final / 2, velocidad_ms, densidad)  # radio = tamano/2

# Impacto según material
if material == "Roca dura":
    diametro, profundidad = impacto_roca_dura(ek_joules)
    radio_km = diametro / 2 / 1000
elif material == "Tierra blanda":
    diam_roca, prof_roca = impacto_roca_dura(ek_joules)
    diametro, profundidad = impacto_tierra_blanda(diam_roca, prof_roca)
    radio_km = diametro / 2 / 1000
else:  # Agua
    altura = impacto_agua(ek_joules, tamano_final / 2)
    radio_km = altura / 1000  # Escala simple

# Generar puntos para mapa
df = generar_puntos_circulo(lat, lon, radio_km)

# ======================
# Mostrar resultados
# ======================
st.subheader("🔍 Resultados de la simulación")
st.write(f"**Tamaño inicial:** {tamano_inicial:.2f} m")
st.write(f"**Tamaño final tras entrar a la atmósfera:** {tamano_final:.2f} m")
st.write(f"**Densidad:** {densidad} kg/m³")
st.write(f"**Velocidad de entrada:** {velocidad_kms:.2f} km/s")
st.write(f"**Material de impacto:** {material}")

if material in ["Roca dura", "Tierra blanda"]:
    st.write(f"**Diámetro estimado:** {diametro:.2f} m")
    st.write(f"**Profundidad estimada:** {profundidad:.2f} m")
else:
    st.write(f"**Altura inicial de la columna de agua:** {altura:.2f} m")

st.write(f"**Radio estimado de impacto para mapa:** {radio_km:.2f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# ======================
# Mostrar mapa
# ======================
st.subheader("🗺️ Mapa de impacto")
mostrar_mapa(df, lat, lon, radio_km)
