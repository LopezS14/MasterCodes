import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import os
import cv2

# Carga de los datos
dataPath = 'dataEmotion'
emotionsList = os.listdir(dataPath)
print('Clasificaciones de emociones: ', emotionsList)

labels = []
faces = []

label = 0

# Carga de las imágenes
for nameDir in emotionsList:
    emotionsPath = os.path.join(dataPath, nameDir)
    for fileName in os.listdir(emotionsPath):
        image = cv2.imread(os.path.join(emotionsPath, fileName), 0)
        if image is not None:
            image = cv2.resize(image, (150, 150), interpolation=cv2.INTER_CUBIC)
            faces.append(image)
            labels.append(label)
    label += 1

faces = np.array(faces)
labels = np.array(labels)

# Redimensionalamos y normalizamos
faces = faces.reshape((faces.shape[0], 150, 150, 1))
faces = faces.astype("float32") / 255.0

# Dividimos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    faces,
    labels,
    test_size=0.2,
    stratify=labels,
    random_state=42
)

# Carga el número de clases
num_classes = len(emotionsList)

# Modelo CNN
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenamos el modelo
print("Entrenando modelo CNN...")
history = model.fit(X_train, y_train, epochs=10, batch_size=32,
                    validation_data=(X_test, y_test))

# Evaluamos el modelo
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Exactitud del modelo: {accuracy*100:.2f}%")

# Realizamos predicciones
y_pred = model.predict(X_test)
y_pred_labels = np.argmax(y_pred, axis=1)

print("Clasification Report:")
print(classification_report(y_test, y_pred_labels, target_names=emotionsList))

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred_labels)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
            xticklabels=emotionsList,
            yticklabels=emotionsList)
plt.title('Matriz de Confusión')
plt.xlabel('Predicción')
plt.ylabel('Valor Real')
plt.tight_layout()
plt.show()
