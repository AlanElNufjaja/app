st.title("Meteorite Visualizer ")

# ...

meteorito_seleccionado = st.sidebar.selectbox("Select a meteorite", opciones)

# ...

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
st.sidebar.write(f"Heat constant: {factor_calor:.1e}")

# ...

st.subheader(" Simulation results")
st.write(f"**Initial size:** {tamano_inicial:.6f} km")
st.write(f"**Final size after atmospheric entry:** {tamano_final:.6f} km")
st.write(f"**Density:** {densidad} kg/m³")
st.write(f"**Impact velocity:** {velocidad_kms:.2f} km/s")
st.write(f"**Crater radius:** {radio_km:.3f} km")
st.write(f"**Impact depth:** {profundidad_m:.3f} km")
st.write(f"**Impact energy:** {energia:.3f} MT")
st.write(f"**Coordinates:** {lat:.4f}, {lon:.4f}")
