import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="🔢 Digit AI",
    page_icon="✏️",
    layout="centered"
)

# =========================
# CARGAR MODELO (CACHE)
# =========================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")

model = load_model()

# =========================
# FUNCIÓN DE PREDICCIÓN
# =========================
def predict_digit(image):
    image = ImageOps.grayscale(image)
    image = image.resize((28, 28))

    img = np.array(image, dtype='float32') / 255.0
    img = img.reshape(1, 28, 28, 1)

    prediction = model.predict(img)
    return np.argmax(prediction)

# =========================
# UI PRINCIPAL
# =========================
st.markdown("<h1 style='text-align:center;'>✏️ Digit Recognizer AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Dibuja un número (0–9) y deja que la IA lo adivine 🤖</p>", unsafe_allow_html=True)

# =========================
# CONTROLES
# =========================
col1, col2 = st.columns(2)

with col1:
    stroke_width = st.slider("🖌️ Grosor", 5, 30, 15)

with col2:
    stroke_color = st.color_picker("🎨 Color", "#FFFFFF")

# =========================
# CANVAS
# =========================
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#000000",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

# =========================
# BOTONES
# =========================
col1, col2 = st.columns(2)

with col1:
    predict_btn = st.button("🔍 Predecir", use_container_width=True)

with col2:
    clear_btn = st.button("🧹 Limpiar", use_container_width=True)

# =========================
# ACCIONES
# =========================
if clear_btn:
    st.rerun()

if predict_btn:
    if canvas_result.image_data is not None:
        image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        result = predict_digit(image)

        st.success(f"🎯 Predicción: *{result}*")

    else:
        st.warning("⚠️ Dibuja un número primero.")

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## ℹ️ Sobre la app")
st.sidebar.write(
"""
Esta aplicación usa una red neuronal para reconocer dígitos escritos a mano.

💡 Tips:
- Dibuja en el centro
- Usa trazos gruesos
- Evita dibujar muy pequeño
"""
)

st.sidebar.markdown("---")
st.sidebar.write("Hecho con ❤️ usando Streamlit")
