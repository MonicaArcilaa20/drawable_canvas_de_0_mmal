import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import random

# 1. Configuración de página con estilo Dark Mode elegante
st.set_page_config(page_title="AI Vision Canvas", layout="wide", page_icon="👁️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        border-radius: 50px; 
        border: 2px solid #4F8BF9;
        transition: all 0.3s;
    }
    .stButton>button:hover { 
        transform: scale(1.05);
        background-color: #4F8BF9;
        color: white;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 15px;
        background: #1e2130;
        border-left: 5px solid #00ffcc;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PREDICCIÓN (La función divertida) ---
def predict_drawing(json_data):
    if json_data is None or len(json_data["objects"]) == 0:
        return "Un lienzo vacío... ¡Qué minimalista!", "😶"
    
    num_objs = len(json_data["objects"])
    types = [obj["type"] for obj in json_data["objects"]]
    
    # Lógica de predicción basada en la estructura del dibujo
    if "circle" in types and num_objs == 1:
        return "Eso es claramente un sol o una pizza sin ingredientes.", "🍕"
    elif num_objs > 15:
        return "Veo un caos absoluto... ¿Es arte abstracto o un plato de espaguetis?", "🍝"
    elif "rect" in types and "line" in types:
        return "Parece una casa o un robot muy cuadrado.", "🤖"
    elif "freedraw" in types and num_objs < 5:
        return "Unas firmas elegantes o quizás el rastro de un caracol.", "🐌"
    else:
        opciones = [
            "¡Es un autorretrato tuyo en el futuro!",
            "Claramente es un mapa de una isla del tesoro.",
            "Una representación cuántica de la felicidad.",
            "¡Un gato! Bueno... un gato dibujado con el pie."
        ]
        return random.choice(opciones), "✨"

# --- SIDEBAR MEJORADO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1004/1004733.png", width=80)
    st.title("Studio Vision")
    st.markdown("---")
    
    with st.expander("🎨 Personalizar Pincel", expanded=True):
        mode = st.selectbox("Herramienta", ("freedraw", "line", "rect", "circle", "transform"))
        stroke_width = st.select_slider("Grosor", options=range(1, 51), value=5)
        stroke_color = st.color_picker("Color del Pincel", "#00FFCC")
        bg_color = st.color_picker("Color del Fondo", "#0E1117")

    if st.button("🗑️ Limpiar Estudio"):
        st.rerun()

# --- CUERPO PRINCIPAL ---
col_main, col_ai = st.columns([3, 1])

with col_main:
    st.subheader("✍️ Área de Creación")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.2)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=550,
        width=850,
        drawing_mode=mode,
        key="main_canvas",
        update_streamlit=True,
    )

with col_ai:
    st.subheader("🧠 IA Predictora")
    st.write("Dibuja algo y deja que la IA lo analice.")
    
    if st.button("🔮 ¿QUÉ ESTOY DIBUJANDO?"):
        if canvas_result.json_data:
            with st.spinner("Analizando pixeles y neuronas..."):
                time.sleep(1.5) # Simula procesamiento
                prediction, icon = predict_drawing(canvas_result.json_data)
                
                st.markdown(f"""
                <div class="prediction-box">
                    <h1 style='font-size: 40px; margin: 0;'>{icon}</h1>
                    <p style='font-size: 18px;'>{prediction}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("¡Primero dibuja algo, artista!")

    st.markdown("---")
    st.write("*Estadísticas del dibujo:*")
    if canvas_result.json_data:
        obj_count = len(canvas_result.json_data["objects"])
        st.write(f"• Elementos detectados: {obj_count}")
        if obj_count > 0:
            st.success("Analizador activo ✅")

# Pie de página
st.markdown("<br><center><p style='color: #555;'>Power by Streamlit & Your Creativity</p></center>", unsafe_allow_html=True)
