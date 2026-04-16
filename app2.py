import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import random

# 1. Configuración de página Futurista
st.set_page_config(page_title="CyberBotanic AI", layout="wide", page_icon="🌿")

# CSS Aesthetic y Futurista
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');
    
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; }
    
    .stButton>button { 
        border-radius: 10px; border: 1px solid #7000ff;
        background: rgba(112, 0, 255, 0.1); color: #00f2ff;
        box-shadow: 0 0 15px rgba(112, 0, 255, 0.3); transition: all 0.4s ease;
    }
    .stButton>button:hover { background: #7000ff; color: white; box-shadow: 0 0 30px #7000ff; transform: translateY(-2px); }
    
    .glass-panel {
        padding: 25px; border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .poem-text {
        font-style: italic; color: #ff00ff; text-shadow: 0 0 5px #ff00ff;
        font-size: 1.2em; border-left: 3px solid #ff00ff; padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'predicted_plant' not in st.session_state: st.session_state.predicted_plant = None
if 'confirmed' not in st.session_state: st.session_state.confirmed = False
if 'tries' not in st.session_state: st.session_state.tries = []

PLANTAS = ["Girasol Neon", "Loto Cuántico", "Rosa de Silicio", "Cactus Binario", "Orquídea Estelar", "Bambú Cibernético"]

def get_new_prediction():
    disponibles = [p for p in PLANTAS if p not in st.session_state.tries]
    if not disponibles: st.session_state.tries = [] # Reset si se acaban
    pred = random.choice(disponibles if disponibles else PLANTAS)
    st.session_state.predicted_plant = pred
    st.session_state.tries.append(pred)

def generate_poem(planta):
    poemas = {
        "Girasol Neon": f"En el jardín de bits, el {planta} gira su rostro hacia el led más brillante. Sus pétalos de oro fundido capturan la energía de un sol que nunca duerme.",
        "Loto Cuántico": f"Sobre las aguas del código binario, el {planta} florece en dos estados a la vez. Es la paz en medio de la tormenta de datos.",
        "Rosa de Silicio": f"Frágil como el cristal, eterna como el cuarzo. La {planta} guarda en sus espinas la memoria de un mundo orgánico ya olvidado.",
        "Cactus Binario": f"Resistente al desierto del hardware, el {planta} almacena bytes de agua. Sus púas son antenas que captan susurros del wifi lejano.",
        "Orquídea Estelar": f"Nacida en el vacío, la {planta} brilla con luz de nebulosa. Sus raíces no buscan tierra, sino gravedad.",
        "Bambú Cibernético": f"Crece rápido entre los cables, el {planta} es flexible ante los virus y fuerte ante el glitch. Un pilar verde en la ciudad de cromo."
    }
    return poemas.get(planta, "Una flora desconocida brota de tus trazos digitales...")

# --- SIDEBAR (Aesthetic) ---
with st.sidebar:
    st.markdown("## 📟 SYSTEM CONTROL")
    with st.expander("🛠️ CONFIG_PINCEL", expanded=True):
        mode = st.selectbox("Tool", ("freedraw", "line", "rect", "circle"))
        s_width = st.slider("Grosor", 1, 30, 4)
        s_color = st.color_picker("Neon Color", "#00F2FF")
        b_color = st.color_picker("Void Color", "#050510")
    
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.confirmed = False
        st.session_state.predicted_plant = None
        st.session_state.tries = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🌿 CYBER-BOTANIC ANALYZER")
st.markdown("---")

col_draw, col_info = st.columns([2.5, 1])

with col_draw:
    st.markdown("### 🖥️ NEURAL CANVAS")
    canvas_result = st_canvas(
        stroke_width=s_width, stroke_color=s_color,
        background_color=b_color, height=500, width=800,
        drawing_mode=mode, key="botanic_canvas",
    )

with col_info:
    st.markdown("### 🧠 AI CORE")
    
    # Botón principal de análisis
    if st.button("🔍 ESCANEAR FORMA BIOLÓGICA"):
        if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
            with st.spinner("Procesando patrones botánicos..."):
                time.sleep(1)
                get_new_prediction()
                st.session_state.confirmed = False
        else:
            st.warning("Canvas vacío. Inserte datos visuales.")

    # Lógica de confirmación
    if st.session_state.predicted_plant:
        st.markdown(f"""
        <div class="glass-panel">
            <p style='color: #888;'>PREDICCIÓN ACTUAL:</p>
            <h2 style='margin: 0;'>{st.session_state.predicted_plant}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.confirmed:
            st.write("¿Es correcta la identificación?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ SÍ"):
                    st.session_state.confirmed = True
                    st.rerun()
            with c2:
                if st.button("❌ NO"):
                    with st.spinner("Recalibrando sensores..."):
                        time.sleep(0.5)
                        get_new_prediction()
                        st.rerun()
        else:
            st.success("Sincronización completa. Canal de poesía abierto.")
            if st.button("✨ GENERAR POEMA CYBERNETIC"):
                poema = generate_poem(st.session_state.predicted_plant)
                st.markdown(f"""
                <div class="glass-panel">
                    <p class="poem-text">{poema}</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

st.markdown("<br><br><p style='text-align: center; color: #444;'>[ SYSTEM_STATUS: ONLINE | ART_MODE: ENABLED ]</p>", unsafe_allow_html=True)
