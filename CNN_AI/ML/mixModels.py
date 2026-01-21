import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix

# Preparar los datos
input_dir = 'CNN_AI/data'
abril_data = os.path.join(input_dir, 'abril')
diciembre_data = os.path.join(input_dir, 'diciembre')
octubre_data = os.path.join(input_dir,'octubre')
febrero_data = os.path.join(input_dir,'febrero')
noviembre_data = os.path.join(input_dir,'noviembre')
categories = ['Raton 1', 'Raton 2', 'Raton C1', 'Raton C2']
data = []
labels = []
for category_idx, category in enumerate(categories):
    for file in os.listdir(os.path.join(input_dir, category)):
        img_path = os.path.join(input_dir, category, file)
        img = imread(img_path)
        img = resize(img, (15, 15))
        data.append(img.flatten())
        labels.append(category_idx)


data = np.asarray(data)
labels = np.asarray(labels)

# División en entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.4, shuffle=True, stratify=labels)

# Entrenar el clasificador
classifier = SVC()

# Parámetros para GridSearchCV
parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

# Ajustar la búsqueda de la cuadrícula 
grid_search = GridSearchCV(classifier, parameters)

# Entrenar el clasificador con los datos de entrenamiento
grid_search.fit(x_train, y_train)

# Obtener el mejor clasificador
best_estimator = grid_search.best_estimator_

# Hacer predicciones
y_prediction = best_estimator.predict(x_test)

# Evaluar la precisión
score = accuracy_score(y_prediction, y_test)
print('{}% de las muestras fueron clasificadas correctamente'.format(str(score * 100)))

# Guardar el modelo entrenado
pickle.dump(best_estimator, open('./model.p', 'wb'))

# Matriz de confusión
cm = confusion_matrix(y_test, y_prediction)

# Visualización de la matriz de confusión
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories)
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()
