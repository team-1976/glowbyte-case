import pandas as pd

# Загрузка данных из CSV файла
df = pd.read_csv('target_train.csv')

# Преобразование столбца с датой/временем в формат datetime
df['Дата'] = pd.to_datetime(df['Дата'])

# Установка столбца с датой/временем в качестве индекса
df.set_index('Дата', inplace=True)

# Интерполяция данных для увеличения частоты записи до каждой минуты
df = df.resample('1Min').interpolate(method='linear')

# Сохранение измененных данных обратно в CSV файл
df.to_csv('augmented_data.csv')