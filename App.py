import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de la página para un look más profesional
st.set_page_config(page_title="Magic Canvas", layout="wide")

st.title("🎨 Magic Canvas Pro")
st.markdown("---")

# Estilos CSS personalizados para mejorar el diseño de los botones y radio
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; }
    .stColorPicker { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🛠️ Herramientas")
    
    with st.expander("📐 Dimensiones", expanded=False):
        canvas_width = st.slider("Ancho", 400, 1000, 800, 50)
        canvas_height = st.slider("Alto", 300, 800, 500, 50)

    st.subheader("🖌️ Pincel")
    drawing_mode = st.selectbox(
        "Herramienta:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point")
    )
    stroke_width = st.slider("Grosor del trazo", 1, 50, 5)

    # --- Sección de Colores Mejorada ---
    st.markdown("---")
    
    # Paletas de colores predefinidas
    palette = ["#FF4B4B", "#FFA500", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#8B00FF", "#FFFFFF", "#000000"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("*Color Pincel*")
        stroke_color = st.color_picker("Stroke", "#FFFFFF", label_visibility="collapsed")
        # Botones rápidos para color de trazo
        st.write("Presets:")
        cp_cols = st.columns(3)
        for i, color in enumerate(palette[:6]):
            if cp_cols[i % 3].button(" ", key=f"p_{i}", help=color):
                stroke_color = color

    with col2:
        st.write("*Color Fondo*")
        bg_color = st.color_picker("BG", "#1E1E1E", label_visibility="collapsed")
        # Botones rápidos para color de fondo
        st.write("Presets:")
        bg_p_cols = st.columns(3)
        bg_presets = ["#FFFFFF", "#1E1E1E", "#2D2D2D"]
        for i, color in enumerate(bg_presets):
            if bg_p_cols[i % 3].button(" ", key=f"bg_{i}", help=color):
                bg_color = color

# --- Área Principal ---
c1, c2, c3 = st.columns([1, 4, 1])

with c2:
    # Contenedor para el canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"canvas_{canvas_width}{canvas_height}{stroke_color}_{bg_color}", 
        update_streamlit=True,
    )

    if canvas_result.image_data is not None:
        st.caption("Usa el botón secundario para guardar tu obra maestra.")
