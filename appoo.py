import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("☄️ Simulador de Impacto de Asteroide")

# Parámetros del usuario
st.sidebar.header("Parámetros del Asteroide")
diametro = st.sidebar.slider("Diámetro (m)", 10, 10000, 500)
velocidad = st.sidebar.slider("Velocidad (km/s)", 1, 70, 30)
angulo = st.sidebar.slider("Ángulo de impacto (°)", 0, 90, 45)

# Simulación de trayectoria
AU_KM = 149597870.7
initial_pos = np.array([0.01 * AU_KM, 0, 0])
angle_rad = np.radians(angulo)
v_vector = np.array([
    -velocidad * np.cos(angle_rad),
    0,
    -velocidad * np.sin(angle_rad)
])
positions = [initial_pos + v_vector * i * 60 for i in range(180)]
positions = np.array(positions)
x, y, z = positions[:,0], positions[:,1], positions[:,2]

# Esfera de la Tierra
theta = np.linspace(0, np.pi, 50)
phi = np.linspace(0, 2 * np.pi, 50)
theta, phi = np.meshgrid(theta, phi)
r = 6371
xe = r * np.sin(theta) * np.cos(phi)
ye = r * np.sin(theta) * np.sin(phi)
ze = r * np.cos(theta)

# Visualización 3D con Plotly
fig = go.Figure()

# Tierra como superficie
fig.add_trace(go.Surface(
    x=xe, y=ye, z=ze,
    colorscale='Blues',
    opacity=0.6,
    showscale=False,
    name='Tierra'
))

# Trayectoria del asteroide
fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines+markers',
    line=dict(color='orange', width=4),
    marker=dict(size=3, color='red'),
    name='Trayectoria'
))

# Punto de impacto
impact_index = np.argmin(np.linalg.norm(positions, axis=1))
impact_x, impact_y, impact_z = positions[impact_index]
fig.add_trace(go.Scatter3d(
    x=[impact_x], y=[impact_y], z=[impact_z],
    mode='markers',
    marker=dict(size=8, color='yellow', symbol='circle'),
    name='Impacto'
))

fig.update_layout(
    title='Trayectoria del Asteroide hacia la Tierra',
    scene=dict(
        xaxis_title='X (km)',
        yaxis_title='Y (km)',
        zaxis_title='Z (km)',
        aspectmode='data'
    ),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
