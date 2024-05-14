import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
import joblib 
# Загрузка данных из CSV файла
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Подготовка данных для предсказания
def prepare_predict_data(data, scaler):
    X = data.drop(columns=['target'])
    X_scaled = scaler.transform(X)
    X_lstm = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])
    return X_lstm

# Загрузка сохраненной модели
model = load_model('my_model2.keras')
scaler = joblib.load('scaler.pkl')  # Путь к сохраненному объекту scaler

# Загрузка данных для предсказания
predict_file_path = 'trimmed_data.csv'  # Замени на путь к файлу с данными для предсказания
predict_data = load_data(predict_file_path)

predict_file_path = 'da2.csv'  # Замени на путь к файлу с данными для предсказания
predict_data2= load_data(predict_file_path)

# Подготовка данных для предсказания
X_predict = prepare_predict_data(predict_data, scaler)

# Предсказание на загруженных данных
predictions = model.predict(X_predict)

# Вывод предсказаний
print("Predictions:")
print(predictions)

# Загрузка целевых значений для тестирования MAE
y_true = predict_data2['target']

# Расчет MAE
mae = mean_absolute_error(y_true, predictions)

# Вывод MAE
print("Mean Absolute Error:", mae)