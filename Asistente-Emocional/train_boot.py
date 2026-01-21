import random
import json
import pickle
import numpy as np
import nltk
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

# Carga de librerías de NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Carga de los intents
with open("intents.json", "r", encoding='utf-8') as f:
    intents = json.load(f)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

# Tokenización y lematización
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))

with open("words.pkl", "wb") as f:
    pickle.dump(words, f)
with open("classes.pkl", "wb") as f:
    pickle.dump(classes, f)

# Creación de los grupos de entrenamiento
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Barajear los grupos de entrenamiento
random.shuffle(training)

# Dividir en training y output
train_x = []
train_y = []

for pattern, tag in training:
    train_x.append(pattern)
    train_y.append(tag)

# Convertir en NumpY
train_x = np.array(train_x)
train_y = np.array(train_y)

# Dividir en entrenamiento y validación (80% - 20%)
train_x_split, val_x, train_y_split, val_y = train_test_split(
    train_x, train_y, test_size=0.2, random_state=42, stratify=train_y
)

# Construcción del modelo de red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.7))
model.add(Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrenamos el modelo con validación
train_process = model.fit(
    train_x_split, train_y_split,
    epochs=100,
    batch_size=5,
    verbose=1,
    validation_data=(val_x, val_y)
)

# Guardamos el modelo junto con el histórico de entrenamiento
model.save("chatbot_model.h5")

# Reporte de evaluación con los datos de entrenamiento completos (opcional)
y_pred = model.predict(train_x)
y_pred_labels = np.argmax(y_pred, axis=1)
y_true_labels = np.argmax(train_y, axis=1)

print("Clasificación:")
report = classification_report(y_true_labels, y_pred_labels, target_names=classes)
print(report)

# Matriz de confusión
cm = confusion_matrix(y_true_labels, y_pred_labels)

# Gráfico de la matriz de confusión
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicho")
plt.ylabel("Valor Real")
plt.title("Matriz de Confusión")
plt.tight_layout()
plt.show()

# Graficar curvas de pérdida y precisión (entrenamiento y validación)
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(train_process.history['loss'], label='Pérdida entrenamiento')
plt.plot(train_process.history['val_loss'], label='Pérdida validación')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(train_process.history['accuracy'], label='Precisión entrenamiento')
plt.plot(train_process.history['val_accuracy'], label='Precisión validación')
plt.title('Precisión durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()

plt.tight_layout()
plt.show()
