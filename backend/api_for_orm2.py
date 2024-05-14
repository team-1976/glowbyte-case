from fastapi import FastAPI, File, UploadFile
import csv
from typing import List, Tuple
import uvicorn
from orm2 import ORM
from datetime import datetime


app = FastAPI()

db_url = 'sqlite:///telemetry.db'  # URL базы данных SQLite
orm = ORM(db_url)



def predict_data(datetime_value: str) -> float:
    # Здесь должен быть наш код для предсказания данных на определенное время
    # Для примера возвращаем случайное значение
    import random
    return random.uniform(0, 100)


def datetime_to_seconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

def parse_csv_data_train(file) -> List[dict]:
    """
    Функция для парсинга CSV файла и преобразования его в массив словарей.
    """
    data = []
    # Пропускаем первую строку (заголовки столбцов)
    next(file.file)
    # Читаем файл строка за строкой, декодируем каждую строку из байтов в строку
    for line in file.file:
        decoded_line = line.decode().strip()
        if decoded_line:
            row = decoded_line.split(',')
            data_row = {'datetime': datetime_to_seconds(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))}
            for i in range(1, len(row)):
                if row[i]:  # Проверяем, что значение не пустое
                    data_row[f'telemetry_{i - 1}'] = float(row[i])
            data.append(data_row)
    orm.load_data_train(data)
    return data


def parse_csv_target(file) -> List[Tuple[str, float]]:

    """

    Функция для парсинга CSV файла и преобразования его в массив кортежей.

    """

    target_array = []

    # Пропускаем первую строку (заголовки столбцов)
    next(file.file)

    # Читаем файл строка за строкой, декодируем каждую строку из байтов в строку
    for line in file.file:
        decoded_line = line.decode().strip()
        if decoded_line:
            row = decoded_line.split(',')
            if len(row) == 2:  # Проверяем, что строка содержит два значения
                try:
                    datetime_value = datetime_to_seconds(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
                    telemetry_value = float(row[1])
                    target_array.append((datetime_value, telemetry_value))
                except (ValueError, IndexError):
                    pass
    print(target_array)
    orm.load_target(target_array)

    return target_array



@app.post("/add_telemetry/")
async def add_telemetry_data(telemetry_data: Dict[str, float]):
    """
    Метод для загрузки данных телеметрии в базу данных.
    """
    try:
        # Добавляем данные телеметрии в базу данных
        orm.add_data_train(datetime_to_seconds((datetime.now())), telemetry_data)
        return {"message": "Данные телеметрии успешно добавлены в базу данных."}
    except Exception as e:
        return {"error": f"Ошибка при добавлении данных телеметрии в базу данных: {e}"}

@app.post("/add_target/")
async def add_target_value(target_value: float):
    """
    Метод для загрузки целевого значения в базу данных.
    """
    try:
        # Добавляем целевое значение в базу данных
        orm.add_target(datetime_to_seconds(datetime.now()), target_value)
        return {"message": "Целевое значение успешно добавлено в базу данных."}
    except Exception as e:
        return {"error": f"Ошибка при добавлении целевого значения в базу данных: {e}"}

@app.post("/upload/data_train")
async def upload_file(file: UploadFile = File(...)):
    """
    API endpoint для загрузки CSV файла и преобразования его в массив словарей.
    """
    if file.filename.endswith('.csv'):
        data = parse_csv_data_train(file)
        return {"data_train_array": data}
    else:
        return {"error": "Invalid file format. Only CSV files are allowed."}

@app.post("/upload/target")
async def upload_file(file: UploadFile = File(...)):
    """
    API endpoint для загрузки CSV файла и преобразования его в массив словарей.
    """
    if file.filename.endswith('.csv'):
        data = parse_csv_target(file)
        return {"data_train_array": data}
    else:
        return {"error": "Invalid file format. Only CSV files are allowed."}


@app.post("/predict/time")
async def predict(datetime_value: str):
    # Предсказываем данные на указанное время
    prediction = predict_data(datetime_value)
    return {"prediction": prediction}

@app.post("/predict/now")
async def predict():
    # Предсказываем данные на этот момент
    return {"prediction": prediction}



@app.post("/predict/history/")
async def prediction_history(start_time: str, end_time: str, step: str) -> List[float]:
    """
    Метод для вывода истории предсказаний на указанный промежуток времени с указанным шагом.
    """
    start_time=int(start_time)
    end_time=int(end_time)
    step=int(step)
    predictions = []
    current_time = start_time
    while current_time <= end_time:
        prediction = predict_data(current_time)
        predictions.append(prediction)
        current_time += step
    return predictions

uvicorn.run(app,host="127.0.0.1",port = 5032)