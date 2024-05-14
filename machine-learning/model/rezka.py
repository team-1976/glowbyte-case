import csv

# Путь к исходному CSV-файлу
csv_file_path = 'da.csv'

# Чтение CSV-файла в массив словарей
array_of_dicts = []
with open(csv_file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        array_of_dicts.append(row)

# Обрезка массива словарей (например, оставим только первые 3 элемента)
array_of_dicts_trimmed = array_of_dicts[0:319]

# Путь к новому CSV-файлу
csv_trimmed_file_path = 'trimmed_data.csv'

# Запись обрезанного массива словарей в новый CSV-файл
with open(csv_trimmed_file_path, 'w', newline='') as csvfile:
    fieldnames = array_of_dicts_trimmed[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in array_of_dicts_trimmed:
        writer.writerow(row)

print(f"Данные успешно записаны в файл: {csv_trimmed_file_path}")