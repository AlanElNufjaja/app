# streamlit_earth.py
import streamlit as st
import pyvista as pv
from pyvista import examples

st.title("🌍 Realistic 3D Earth Viewer")

# Load Earth model
mesh = pv.read("tierra.glb")  # Replace with your downloaded model
texture = pv.read_texture("tierra.jpg")

# Create plotter
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(mesh, texture=texture)
plotter.set_background("black")
plotter.camera_position = 'yz'  # Adjust view angle

# Render to image
img = plotter.screenshot()

# Display in Streamlit
st.image(img, caption="Earth Model with Texture", use_column_width=True)
