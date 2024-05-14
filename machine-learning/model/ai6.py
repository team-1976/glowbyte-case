import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import keras
import joblib

# Загрузка данных из CSV файла
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Подготовка данных для обучения модели
def prepare_data(data):
    # Разделение на признаки (X) и целевую переменную (y)
    X = data.drop(columns=['target'])
    y = data['target']

    # Масштабирование признаков
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'scaler.pkl')

    # Преобразование данных в трехмерный массив для использования в LSTM
    X_lstm = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])

    return X_lstm, y, scaler

# Создание и обучение модели LSTM
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Обучение модели
def train_model(model, X_train, y_train, epochs=10, batch_size=32):
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

# Загрузка данных
file_path = 'output_without_nan.csv'
data = load_data(file_path)

# Подготовка данных
X, y, scaler = prepare_data(data)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели LSTM
input_shape = (X_train.shape[1], X_train.shape[2])
model = create_lstm_model(input_shape)
train_model(model, X_train, y_train)

# Оценка модели на тестовой выборке
loss = model.evaluate(X_test, y_test)
print("Test Loss:", loss)

keras.saving.save_model(model, 'my_model2.keras')


'''
from sklearn.metrics import mean_absolute_error

# Загрузка данных для тестирования
test_file_path = 'test_data.csv'
test_data = load_data(test_file_path)

# Подготовка данных для тестирования
X_test, y_test, _ = prepare_data(test_data)

# Прогнозирование на тестовых данных
y_pred = model.predict(X_test)

# Расчет средней абсолютной ошибки (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
'''