# main.py
from datetime import datetime
from orm2 import ORM

# Создаем объект ORM
db_url = 'sqlite:///telemetry.db'  # URL базы данных SQLite
orm = ORM(db_url)

# Пример добавления данных в таблицы
telemetry_data = {
    'telemetry_0': 1.1,
    'telemetry_1': 2.2,
    # Добавьте остальные значения телеметрии
}
target_value = 42.0


def datetime_to_seconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())

# Пример использования
dt = datetime.now()
seconds = datetime_to_seconds(dt)
print("Seconds since epoch:", seconds)

#orm.add_data_train(seconds, telemetry_data)
#orm.add_target(seconds, target_value)

# Пример массива данных для таблицы data_train
data_train_array = [
    {'datetime': datetime_to_seconds(datetime.now()), 'telemetry_0': 1.1, 'telemetry_1': 2.2, 'telemetry_2': 3.3},
    {'datetime': datetime_to_seconds(datetime.now()), 'telemetry_0': 4.4, 'telemetry_1': 5.5, 'telemetry_2': 6.6},
    # Добавьте другие данные, если необходимо
]

# Пример массива данных для таблицы target
target_array = [
    (datetime_to_seconds(datetime.now()), 42.0),
    (datetime_to_seconds(datetime.now()), 43.0),
    # Добавьте другие данные, если необходимо
]

#orm.load_data_train(data_train_array)
#orm.load_target(target_array)

start_time = 1715590555
end_time = 1715590554 
data_train_by_time_range = orm.read_data_train_by_time_range(start_time, end_time)
target_by_time_range = orm.read_target_by_time_range(start_time, end_time)

# Пример чтения данных по идентификаторам в заданном диапазоне
start_id = 1
end_id = 100
data_train_by_id_range = orm.read_data_train_by_id_range(start_id, end_id)
target_by_id_range = orm.read_target_by_id_range(start_id, end_id)

print(data_train_by_time_range)
print(data_train_by_id_range)
print(data_train_array)
print(target_by_time_range)
print(target_by_id_range[0])

orm.close()
