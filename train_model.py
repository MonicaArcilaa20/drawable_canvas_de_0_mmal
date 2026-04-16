import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# =========================
# CARGAR DATASET (MNIST)
# =========================
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# Añadir canal (para CNN)
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

# =========================
# MODELO (ligero y potente)
# =========================
model = keras.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    layers.MaxPooling2D(),
    
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])

# =========================
# COMPILAR
# =========================
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# =========================
# ENTRENAR
# =========================
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# =========================
# GUARDAR (FORMATO PRO)
# =========================
model.save("model.keras")

print("✅ Modelo guardado como model.keras")
