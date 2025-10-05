elif tipodano == "Sonido":
    capa_negra = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[0, 0, 255, 50],  # Opacidad más baja
        get_radius=radio_km * 750,
        pickable=False,
        get_line_color=[0, 0, 0, 255],  
        get_line_width=1
    )
    capa_rojo = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[0, 0, 200, 50],  
        get_radius=radio_km * 600,  # Radio diferente
        pickable=False,
        get_line_color=[0, 0, 200, 255],  
        get_line_width=1
    )
    capa_naranja = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[0, 128, 255, 50],  
        get_radius=radio_km * 450,  # Radio diferente
        pickable=False,
        get_line_color=[0, 128, 255, 255],  
        get_line_width=1
    )
    capa_amarillo = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[128, 255, 255, 50],  
        get_radius=radio_km * 300,  # Radio diferente
        pickable=False,
        get_line_color=[128, 255, 255, 255],  
        get_line_width=1
    )
    layers = [capa_negra, capa_rojo, capa_naranja, capa_amarillo]
