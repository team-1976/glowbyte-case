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
    X = data
    X_scaled = scaler.transform(X)
    X_lstm = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])
    return X_lstm

def ai_request(data_name,target_name):
	# Загрузка сохраненной модели
	model = load_model('my_model2.keras')
	scaler = joblib.load('scaler.pkl')  # Путь к сохраненному объекту scaler

	# Загрузка данных для предсказания
	predict_file_path = "out.csv"
	import pandas as pd

	df2 = pd.read_csv(data_name)
	data_list2 = df2.to_dict(orient='records')
	filtered_data_list2 = [d for d in data_list2 if not any(pd.isna(value) for value in d.values())]

	from datetime import datetime
	for d in filtered_data_list2:
	    if 'datetime' in d:
	        try:
	            d['datetime'] = int(datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S').timestamp())
	        except ValueError:
	            pass

	for d in filtered_data_list2:
	    for key in ['telemetry_12', 'telemetry_13', 'telemetry_14', 'telemetry_15']:
	        if key in d:
	            del d[key]
	import csv
	with open("da.csv", 'w', newline='') as csvfile:
	    fieldnames = filtered_data_list2[0].keys()
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for row in filtered_data_list2:
	        writer.writerow(row)
	'''
	# Загрузка данных из первого CSV файла в массив словарей
	df1 = pd.read_csv('da.csv')
	data_list1 = df1.to_dict(orient='records')

	# Загрузка данных из второго CSV файла в массив словарей
	df2 = pd.read_csv('da2.csv')
	data_list2 = df2.to_dict(orient='records')

	data_list1 = data_list1[:len(data_list2)]

	ids_set1 = set(d['datetime'] for d in data_list1)
	ids_set2 = set(d['datetime'] for d in data_list2)
	koj = []
	lll = []
	for l in data_list2:
	    if l['datetime'] in ids_set1 and l['datetime'] not in lll:
	        koj.append(l)
	        lll.append(l['datetime'])

	df2 = pd.read_csv(target_name)
	data_list2 = df2.to_dict(orient='records')
	filtered_data_list2 = [d for d in data_list2 if not any(pd.isna(value) for value in d.values())]
	print(filtered_data_list2)

	from datetime import datetime
	for d in filtered_data_list2:
	    if 'Дата' in d:
	        try:
	            d['datetime'] = int(datetime.strptime(d['Дата'], '%Y-%m-%d %H:%M:%S').timestamp())
	        except ValueError:
	            pass


	csv_file_path = 'da2.csv'

	# Запись данных в CSV файл
	with open(csv_file_path, 'w', newline='') as csvfile:
	    fieldnames = ['datetime', 'target']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for row in filtered_data_list2:
	        writer.writerow({'datetime': row['datetime'], 'target': row['target']})

	print(f"Данные успешно записаны в файл: {csv_file_path}")


	'''
	# Загрузка данных из первого CSV файла в массив словарей
	df1 = pd.read_csv('da2.csv')
	data_list1 = df1.to_dict(orient='records')

	# Загрузка данных из второго CSV файла в массив словарей
	df2 = pd.read_csv('da.csv')
	data_list2 = df2.to_dict(orient='records')


	'''


	ids_set1 = set(d['datetime'] for d in data_list1)
	ids_set2 = set(d['datetime'] for d in data_list2)
	koj = []
	lll = []
	for l in data_list2:
	    if l['datetime'] in ids_set1 and l['datetime'] not in lll:
	        koj.append(l)
	        lll.append(l['datetime'])
	df = pd.DataFrame(koj)

	# Сохраняем DataFrame в CSV файл
	df.to_csv('output.csv', index=False)

	'''
	data_list1 = data_list1[:len(data_list2)]





	#df1 = pd.read_csv('target_train.csv')
	predict_data = load_data('output.csv')
	preduct_data = pd.DataFrame(data_list1)
	#print(predict_data[0])
	#print(data_list1[0])
	predict_data=data_list1
	#print(predict_data)
	#print(len(predict_data))

	# Подготовка данных для предсказания
	#X_predict = prepare_predict_data(predict_data, scaler)
	X_predict = prepare_predict_data(predict_data, scaler)

	# Предсказание на загруженных данных
	predictions = model.predict(X_predict)


	# Вывод предсказаний
	print("Predictions:")
	print(predictions)

	# Загрузка целевых значений для тестирования MAE
	ppp = load_data('da2.csv')
	print(len(predictions))
	y_true = ppp['target'][0:len(predictions)]
	ffll = len(y_true)
	# Расчет MAE
	mae = mean_absolute_error(y_true, predictions)

	# Вывод MAE
	print("Mean Absolute Error:", mae)

	return [mae,predictions]

ai_request("data_test_small.csv","target_test_small.csv")