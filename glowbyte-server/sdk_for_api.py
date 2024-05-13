import requests
from typing import List, Tuple,Dict

class TelemetrySDK:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def upload_data_train(self, file_path: str) -> List[dict]:
        url = f"{self.base_url}/upload/data_train"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.json()["data_train_array"]
        else:
            print("Ошибка при загрузке файла:", response.text)
            return []

    def upload_target(self, file_path: str) -> List[Tuple[str, float]]:
        url = f"{self.base_url}/upload/target"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.json()["data_train_array"]
        else:
            print("Ошибка при загрузке файла:", response.text)
            return []

    def predict_at_time(self, datetime_value: str) -> float:
        url = f"{self.base_url}/predict/a"
        payload = {"datetime_value": datetime_value}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["prediction"]
        else:
            print("Ошибка при предсказании:", response.text)
            return None

    def predict_current_time(self) -> float:
        url = f"{self.base_url}/predict/now"
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()["prediction"]
        else:
            print("Ошибка при предсказании:", response.text)
            return None

    def prediction_history(self, start_time: str, end_time: str, step: str) -> List[float]:
        url = f"{self.base_url}/predict/history/"
        payload = {"start_time": start_time, "end_time": end_time, "step": step}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении истории предсказаний:", response.text)
            return []

    def add_telemetry_data(self, telemetry_data: Dict[str, float]) -> Dict:
        url = f"{self.base_url}/add_telemetry/"
        response = requests.post(url, json=telemetry_data)
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при добавлении данных телеметрии:", response.text)
            return {}

    def add_target_value(self, target_value: float) -> Dict:
        url = f"{self.base_url}/add_target/"
        payload = {"target_value": target_value}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при добавлении целевого значения:", response.text)
            return {}
#использование sdk
sdk = TelemetrySDK("http://127.0.0.1:5032")
#Загрузка актуального значения таргетов
sdk.add_telemetry_data(3.3)
#Загрузка актуальных значений датчиков
sdk.add_telemetry_data({})

# Загрузка данных тренировки
data_train_array = sdk.upload_data_train("data_train.csv")

# Загрузка целевых данных
target_array = sdk.upload_target("target.csv")

# Предсказание на указанное время
prediction_at_time = sdk.predict_at_time("2024-05-14 12:00:00")

# Предсказание на текущий момент
prediction_current_time = sdk.predict_current_time()

# Получение истории предсказаний
prediction_history = sdk.prediction_history("0", "100", "10")
