import streamlit as st
import requests
import matplotlib as pd
# Функция для загрузки CSV файла на сервер
def upload_csv(url, file):
    files = {'file': file}
    response = requests.post(url, files=files)
    return response.json()

# URL для загрузки данных обучения и целевой переменной
upload_data_train_url = "http://127.0.0.1:8000/upload/data_train"
upload_target_url = "http://127.0.0.1:8000/upload/target"

# Загрузка CSV файлов и получение данных
def load_data_train():
    uploaded_file = st.file_uploader("Upload Training Data CSV")
    if uploaded_file is not None:
        data = upload_csv(upload_data_train_url, uploaded_file)
        return data

def load_target():
    uploaded_file = st.file_uploader("Upload Target CSV")
    if uploaded_file is not None:
        data = upload_csv(upload_target_url, uploaded_file)
        return data

# Загрузка данных обучения и целевой переменной
data_train = load_data_train()
target = load_target()





# Кнопка для запуска предсказания
if st.button("Run Prediction"):
    if data_train is not None and target is not None:
        # Ваш код для запуска предсказания
        # В этом блоке можно вызвать вашу функцию для предсказания на основе загруженных данных
        # и вывести результат
        st.write("Prediction Successful!")
    else:
        st.write("Please upload both Training Data and Target CSV files.")

