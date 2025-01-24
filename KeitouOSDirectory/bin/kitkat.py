import os
import requests
import argparse
import sys
import time

REPO_URL = "https://raw.githubusercontent.com/izawokakawo/keitourepo/main"  # URL для доступа к файлам
API_URL = "https://api.github.com/repos/izawokakawo/keitourepo/contents"  # URL для доступа к API
TARGET_DIRECTORY = "KeitouOSDirectory/usr"

def ensure_target_directory():
    """Создает целевую директорию, если она не существует."""
    os.makedirs(TARGET_DIRECTORY, exist_ok=True)

def download_package(package_name):
    target_path = os.path.join(TARGET_DIRECTORY, f"{package_name}.py")
    
    # Удаляем старую версию, если она существует
    if os.path.exists(target_path):
        os.remove(target_path)
    
    # Формируем URL для загрузки файла
    file_url = f"{REPO_URL}/{package_name}.py"
    
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Проверяем, что запрос успешен
        
        # Получаем общий размер файла для индикатора прогресса
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # Сохраняем файл в целевую директорию с индикатором прогресса
        with open(target_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                downloaded_size += len(data)
                # Обновляем индикатор прогресса
                progress = downloaded_size / total_size * 100
                print(f"\rСкачивание {package_name}: [{'#' * int(progress // 2):<50}] - {progress:.2f}%", end="")
        
        print()  # Переход на новую строку после завершения загрузки
        print(f"Пакет {package_name} успешно установлен.")
    except requests.HTTPError:
        print(f"Пакет {package_name} не найден в репозитории.")
    except Exception as e:
        print(f"Произошла ошибка при загрузке пакета: {e}")

def update_package(package_name):
    target_path = os.path.join(TARGET_DIRECTORY, f"{package_name}.py")
    
    if os.path.exists(target_path):
        download_package(package_name)  # Просто перезагружаем файл
    else:
        print(f"Пакет {package_name} не установлен. Установите его с помощью команды 'kitkat install {package_name}'.")

def list_packages():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверяем, что запрос успешен
        
        packages = [item['name'] for item in response.json() if item['name'].endswith('.py')]
        
        if packages:
            print("Доступные пакеты:")
            for package in packages:
                print(f" - {package[:-3]}")  # Убираем .py из имени
        else:
            print("Нет доступных пакетов.")
    except Exception as e:
        print(f"Произошла ошибка при получении списка пакетов: {e}")

def update_all_packages():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверяем, что запрос успешен
        
        packages = [item['name'] for item in response.json() if item['name'].endswith('.py')]
        
        if packages:
            print("Обновление всех пакетов...")
            for package in packages:
                update_package(package[:-3])  # Убираем .py из имени
        else:
            print("Нет доступных пакетов для обновления.")
    except Exception as e:
        print(f"Произошла ошибка при получении списка пакетов: {e}")

def main():
    ensure_target_directory()  # Убедимся, что целевая директория существует

    parser = argparse.ArgumentParser(description='Пакетный менеджер KitKat для KeitouOS')
    parser.add_argument('command', choices=['install', 'update', 'list', 'update-all'], help='Команда для выполнения')
    parser.add_argument('package', nargs='?', help='Имя пакета (без .py)')

    args = parser.parse_args()

    if args.command == 'install' and args.package:
        download_package(args.package)
    elif args.command == 'update' and args.package:
        update_package(args.package)
    elif args.command == 'list':
        list_packages()
    elif args.command == 'update-all':
        update_all_packages()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
