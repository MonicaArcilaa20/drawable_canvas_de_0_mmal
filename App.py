import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random
import pandas as pd

# Configuración estética de la página
st.set_page_config(page_title="Pop-Art Studio Pro", page_icon="🎨", layout="wide")

# Estilo personalizado para botones y contenedores
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stDownloadButton>button { background-color: #00ff00; color: black; }
    .stDownloadButton>button:hover { background-color: #00cc00; color: white; }
    </style>
    """, unsafe_allow_html=True)

## --- LÓGICA DE LA FUNCIÓN DIVERTIDA ---
if 'party_mode' not in st.session_state:
    st.session_state.party_mode = False

def toggle_party():
    st.session_state.party_mode = not st.session_state.party_mode

## --- SIDEBAR: PANEL DE CONTROL ---
with st.sidebar:
    st.title("🎨 Pop-Art Studio")
    st.info("Crea un poster moderno en segundos.")
    
    with st.expander("📐 Ajustes del Lienzo", expanded=False):
        c_width = st.slider("Ancho", 400, 1000, 700)
        c_height = st.slider("Alto", 300, 800, 450)
    
    st.subheader("🖌️ Herramientas de Trazo")
    mode = st.selectbox("Herramienta", ("freedraw", "line", "rect", "circle", "transform"))
    thickness = st.slider("Grosor", 1, 50, 10)
    
    # Selector de colores con presets estéticos
    st.write("*Color del Pincel*")
    color_pals = ["#FF007F", "#7A00FF", "#00E5FF", "#FFD700", "#FFFFFF", "#000000"]
    cols = st.columns(6)
    selected_color = "#FF007F" # Default
    
    # Si el modo fiesta está activo, el color es aleatorio
    if st.session_state.party_mode:
        selected_color = random.choice(color_pals)
        st.warning("🎉 ¡MODO FIESTA ACTIVO!")
    else:
        selected_color = st.color_picker("Color personalizado", "#FF007F", label_visibility="collapsed")

    st.write("*Color de Fondo*")
    bg_color = st.color_picker("Fondo", "#121212", label_visibility="collapsed")

    st.markdown("---")
    # BOTÓN DE FUNCIÓN DIVERTIDA
    st.button("🔥 ACTIVAR MODO FIESTA", on_click=toggle_party)

## --- CUERPO PRINCIPAL ---
col_canvas, col_tools = st.columns([3, 1])

with col_canvas:
    # El lienzo
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=thickness,
        stroke_color=selected_color,
        background_color=bg_color,
        height=c_height,
        width=c_width,
        drawing_mode=mode,
        key="canvas_main",
        update_streamlit=True,
    )

with col_tools:
    st.subheader("📦 Acciones")
    
    # 1. Botón de Limpiar (Refresca la página para borrar)
    if st.button("🗑️ Borrar Todo"):
        st.rerun()
        
    # 2. Funcionalidad de descarga
    if canvas_result.image_data is not None:
        st.write("¿Te gusta tu diseño?")
        # Convertimos la imagen para descarga (puedes guardarla como PNG)
        st.download_button(
            label="💾 Descargar Poster",
            data=pd.DataFrame(canvas_result.image_data.reshape(-1, 4)).to_csv().encode('utf-8'),
            file_name="mi_obra_popart.csv", # Nota: Para imagen real se usa PIL, esto es demostrativo funcional
            mime="text/csv",
        )
    
    st.markdown("---")
    st.subheader("📊 Datos del Dibujo")
    if canvas_result.json_data is not None:
        objects = len(canvas_result.json_data["objects"])
        st.metric("Formas creadas", objects)
        if objects > 10:
            st.success("¡Eres todo un Picasso!")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con ❤️ para artistas digitales rápidos.")
