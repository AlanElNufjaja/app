import streamlit as st
import pandas as pd
from parameters import obtener_coordenadas, velocidad_realista, calcular_radio_impacto
from damage import generar_puntos_circulo
from mapa import mostrar_mapa

st.title("Visualizador de Meteoritos 2D ☄️")

# ======================
# Función para calcular pérdida de tamaño
# ======================
def perdida_tamano_meteorito(densidad, velocidad, tamano_inicial):
    """
    Calcula la pérdida aproximada de tamaño de un meteorito al entrar en la atmósfera.
    Parámetros:
      densidad: densidad del meteorito (kg/m³)
      velocidad: velocidad de entrada (m/s)
      tamano_inicial: diámetro inicial del meteorito (m)
    Retorna:
      tamaño final estimado (m)
    """
    coef_resistencia = 0.47        # coeficiente de arrastre (esfera)
    densidad_aire = 1.225           # kg/m³ al nivel del mar
    factor_calor = 1e-8             # constante ajustable (representa pérdida térmica)
    
    energia = 0.5 * densidad * (velocidad**2)
    area = 3.1416 * (tamano_inicial / 2)**2
    perdida_tamano = factor_calor * energia * area / densidad
    tamano_final = max(tamano_inicial - perdida_tamano, 0)
    
    return tamano_final

# ======================
# Cargar datos
# ======================
datos_base = pd.read_csv("datos_base.csv")
datos_limpios = pd.read_csv("datos_limpios.csv")

meteoritos = pd.concat([datos_base, datos_limpios], axis=1)
opciones = meteoritos['id'].astype(str).tolist()
meteorito_seleccionado = st.sidebar.selectbox("Selecciona un meteorito", opciones)

mete = meteoritos[meteoritos['id'].astype(str) == meteorito_seleccionado].iloc[0]

# Datos predeterminados del meteorito seleccionado
tamano_inicial = (
    (mete['estimated_diameter.kilometers.estimated_diameter_min'] +
     mete['estimated_diameter.kilometers.estimated_diameter_max']) / 2
) * 1000  # km → m

densidad = 3000  # kg/m³ estándar
velocidad_kms = mete['relative_velocity.kilometers_per_second']

# ======================
# Entradas del usuario
# ======================
lugar = st.sidebar.text_input("Nombre de la ciudad")
lat_manual = st.sidebar.slider("Latitud manual", float(-80), float(80), 19.44, step=0.0001)
lon_manual = st.sidebar.slider("Longitud manual", float(-180), float(180), -99.1, step=0.0001)

tamano_inicial = st.sidebar.slider("Tamaño del meteorito (m)", 0.1, 500.0, float(tamano_inicial))
densidad = st.sidebar.slider("Densidad (kg/m³)", 1000, 8000, int(densidad))

# ======================
# Cálculos principales
# ======================
lat, lon = obtener_coordenadas(lugar, lat_manual, lon_manual)

# Convertir velocidad a m/s para el cálculo físico
velocidad_ms = velocidad_kms * 1000

# Calcular tamaño final tras pérdida
tamano_final = perdida_tamano_meteorito(densidad, velocidad_ms, tamano_inicial)

# Calcular radio de impacto con el tamaño reducido
radio_km = calcular_radio_impacto(tamano_final, densidad, velocidad_kms)

# Generar puntos de impacto (centro y radio)
df = generar_puntos_circulo(lat, lon, radio_km)

# ======================
# Mostrar resultados
# ======================
st.write(f"**Tamaño inicial:** {tamano_inicial:.1f} m")
st.write(f"**Tamaño final estimado tras entrar a la atmósfera:** {tamano_final:.2f} m")
st.write(f"**Densidad:** {densidad} kg/m³")
st.write(f"**Velocidad de impacto:** {velocidad_kms:.2f} km/s")
st.write(f"**Radio estimado de impacto:** {radio_km:.2f} km")
st.write(f"**Coordenadas:** {lat:.4f}, {lon:.4f}")

# ======================
# Mostrar mapa
# ======================
mostrar_mapa(df, lat, lon, radio_km)
