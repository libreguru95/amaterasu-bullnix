import os
import subprocess

# Указываем путь к директории, где находятся Python файлы
directory_path = 'KeitouOSDirectory/usr'

# Получаем список файлов в указанной директории
try:
    files = os.listdir(directory_path)
except FileNotFoundError:
    print(f"Директория {directory_path} не найдена.")
    exit(1)

# Фильтруем файлы, оставляя только файлы с расширением .py
python_files = [f for f in files if f.endswith('.py')]

# Проверяем, есть ли файлы с расширением .py
if python_files:
    print("Выберите файл для открытия:")
    for index, file in enumerate(python_files):
        print(f"{index + 1}: {file}")

    # Запрашиваем у пользователя выбор файла
    choice = input("Введите номер файла: ")

    try:
        # Преобразуем выбор в индекс
        file_index = int(choice) - 1

        if 0 <= file_index < len(python_files):
            file_to_open = os.path.join(directory_path, python_files[file_index])
            print(f"Открытие файла: {file_to_open}")

            # Используем subprocess для запуска файла
            subprocess.run(['python', file_to_open])  # или ['python3', file_to_open] для Python 3
        else:
            print("Неверный номер файла.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")
else:
    print("В директории нет файлов с расширением .py.")
