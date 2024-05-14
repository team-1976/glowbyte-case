import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras


# Загрузка данных из CSV файла
data = pd.read_csv('output_without_nan.csv')

# Разделение данных на признаки (X) и целевую переменную (y)
X = data.iloc[:, 1:13]  # Признаки от 1 до 12 столбца
y = data.iloc[:, 13]     # Целевая переменная - 13 столбец
print(y)

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Масштабирование признаков
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Создание модели Sequential
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(12,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Компиляция модели
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Обучение модели
model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Оценка модели на тестовом наборе
loss, mae = model.evaluate(X_test_scaled, y_test)
print("Test Mean Absolute Error:", mae)

keras.saving.save_model(model, 'my_model.keras')

