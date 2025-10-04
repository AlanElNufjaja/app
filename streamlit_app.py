# streamlit_app.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import folium

st.title("🌍 Asteroid Impact Simulator")

# User inputs
size = st.slider("Asteroid Diameter (m)", 10, 10000, 500)
velocity = st.slider("Velocity (km/s)", 1, 70, 30)
angle = st.slider("Impact Angle (°)", 0, 90, 45)

# Simulate trajectory
AU_KM = 149597870.7
initial_pos = np.array([0.01 * AU_KM, 0, 0])
v_vector = np.array([-velocity, 0, 0])
positions = [initial_pos + v_vector * i * 60 for i in range(180)]
positions = np.array(positions)

# Plotly 3D visualization
fig = go.Figure()
fig.add_trace(go.Scatter3d(x=positions[:,0], y=positions[:,1], z=positions[:,2],
    mode='lines', line=dict(color='orange', width=4), name='Asteroid Path'))
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0],
    mode='markers', marker=dict(size=10, color='blue'), name='Earth'))
st.plotly_chart(fig)

# Folium map
impact_lat, impact_lon = 20.5, -89.5
m = folium.Map(location=[impact_lat, impact_lon], zoom_start=6)
folium.Marker([impact_lat, impact_lon], popup="Impact Site").add_to(m)
folium.Circle([impact_lat, impact_lon], radius=size * 100, color="red", fill=True).add_to(m)
st.components.v1.html(m._repr_html_(), height=500)
