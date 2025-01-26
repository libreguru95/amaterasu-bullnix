import os
import json
import time
import urllib.request
import sys
import subprocess

class SystemInit:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.run_systeminit()

    def run_systeminit(self):
        systeminit_script = os.path.join(self.base_directory, "bin", "systeminit.py")
        os.system(f"python {systeminit_script}")

        
class amaterasu:
    def __init__(self):
        self.base_directory = "amaterasudir"
        self.create_directory_structure()
        self.username = self.load_username()
        self.home_directory = os.path.join(self.base_directory, "home", self.username)
        self.create_home_directory()  # Создаем домашнюю директорию
        self.current_directory = self.home_directory  # Текущая директория
        
        self.installed_packages = self.load_installed_packages()
        
        self.color_scheme = "default"
        self.plugins = self.load_plugins()
        self.file_permissions = {}  # Система прав доступа
        self.sudoers = self.load_sudoers()  # Загрузка списка пользователей с правами
        self.load_commands()

        # Запускаем инициализацию системы
        SystemInit(self.base_directory)

    def create_home_directory(self):
        os.makedirs(self.home_directory, exist_ok=True)  # Создаем домашнюю директорию
        
    def create_directory_structure(self):
        os.makedirs(self.base_directory, exist_ok=True)
        subdirectories = ["bin", "opt", "etc", "usr", "var", "home"]
        for subdir in subdirectories:
            os.makedirs(os.path.join(self.base_directory, subdir), exist_ok=True)
        # Создаем файл sudoers, если он не существует
        sudoers_file = os.path.join(self.base_directory, "etc", "sudoers")
        if not os.path.exists(sudoers_file):
            with open(sudoers_file, "w") as f:
                f.write("toor\n")  # Добавляем пользователя toor по умолчанию
                
    def load_username(self):
        username_file = os.path.join(self.base_directory, "username.txt")
        if os.path.exists(username_file):
            with open(username_file, "r") as f:
                return f.read().strip()
        else:
            return input("Enter your username: ")
        
    def load_username(self):
        username_file = os.path.join(self.base_directory, "username.txt")
        if os.path.exists(username_file):
            with open(username_file, "r") as f:
                return f.read().strip()
        else:
            username = input("Enter your username: ")
            with open(username_file, "w") as f:
                f.write(username)
            return username

    def load_sudoers(self):
        sudoers_file = os.path.join(self.base_directory, "etc", "sudoers")
        if os.path.exists(sudoers_file):
            with open(sudoers_file, "r") as f:
                return [line.strip() for line in f.readlines()]
        return []

    def load_installed_packages(self):
        installed_packages_file = os.path.join(self.base_directory, "installed_packages.txt")
        if os.path.exists(installed_packages_file):
            with open(installed_packages_file, "r") as f:
                return [line.strip() for line in f.readlines()]
        return []

    def save_installed_packages(self):
        installed_packages_file = os.path.join(self.base_directory, "installed_packages.txt")
        with open(installed_packages_file, "w") as f:
            for pkg in self.installed_packages:
                f.write(pkg + "\n")

    def load_plugins(self):
        plugins_file = os.path.join(self.base_directory, "plugins.json")
        if os.path.exists(plugins_file):
            with open(plugins_file, "r") as f:
                return json.load(f)
        return {}

    def save_plugins(self):
        plugins_file = os.path.join(self.base_directory, "plugins.json")
        with open(plugins_file, "w") as f:
            json.dump(self.plugins, f)

    def run(self):
        print("Welcome to Amaterasu Bullnix")
        while True:
            if self.username == "toor":
                command = input(f"{self.username}@amaterasu:~# ")  # Для пользователя toor
            else:
                command = input(f"{self.username}@amaterasu:~$ ")  # Для остальных пользователей
            self.execute_command(command)



    def load_commands(self):
        with open('commands.json', 'r') as f:
            self.commands = json.load(f)['commands']

    def execute_command(self, command):
        for cmd in self.commands:
            if command.startswith(cmd['name']):
                args = command.split(" ")[1:1 + cmd['args']]
                method = getattr(self, cmd['method'], None)
                if method:
                    method(*args)
                return
        print("Unknown command")

    def change_directory(self, dirname):
        new_directory = os.path.join(self.current_directory, dirname)
        
        if dirname == "..":
            new_directory = os.path.dirname(self.current_directory)
        elif os.path.isabs(dirname):
            new_directory = dirname

        if os.path.isdir(new_directory):
            self.current_directory = new_directory
            print(f"Changed directory to: {self.current_directory}")
        else:
            print(f"Directory '{dirname}' not found.")

    def make_directory(self, dirname):
        dir_path = os.path.join(self.current_directory, dirname)
        try:
            os.makedirs(dir_path, exist_ok=False)
            self.file_permissions[dirname] = {"owner": self.username, "read": True, "write": True}
            print(f"Directory '{dirname}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dirname}' already exists.")

    def remove_file(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        if self.check_permissions(file_path, "write"):
            try:
                os.remove(file_path)
                del self.file_permissions[filename]
                print(f"File '{filename}' removed successfully.")
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except IsADirectoryError:
                print(f"'{filename}' is a directory. Use 'rm -r' to remove directories.")
        else:
            print(f"You do not have permission to remove '{filename}'.")

    def move_file(self, src, dest):
        src_path = os.path.join(self.current_directory, src)
        dest_path = os.path.join(self.current_directory, dest)
        if self.check_permissions(src_path, "write"):
            try:
                os.rename(src_path, dest_path)
                self.file_permissions[dest] = self.file_permissions.pop(src)  # Перенос прав
                print(f"Moved '{src}' to '{dest}'.")
            except FileNotFoundError:
                print(f"File '{src}' not found.")
            except FileExistsError:
                print(f"Destination '{dest}' already exists.")
        else:
            print(f"You do not have permission to move '{src}'.")

    def list_directory_contents(self):
        print("Contents of the current directory:")
        for item in os.listdir(self.current_directory):
            print(f"- {item}")

    def change_color_scheme(self, color):
        if color in ["default", "red", "green", "blue"]:
            self.color_scheme = color
            print(f"Color scheme changed to '{color}'.")
        else:
            print(f"Color '{color}' is not a valid option.")

    def install_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            self.plugins[plugin_name] = {"installed": True}
            self.save_plugins()
            print(f"Plugin '{plugin_name}' installed successfully.")
        else:
            print(f"Plugin '{plugin_name}' is already installed.")

    def remove_package(self, package_name):
        if package_name in self.installed_packages:
            self.installed_packages.remove(package_name)
            self.save_installed_packages()
            print(f"Package '{package_name}' removed successfully.")
        else:
            print(f"Package '{package_name}' is not installed.")

    def search_package(self, query):
        print("Searching for packages...")
        found_packages = [pkg for pkg in self.available_packages if query in pkg]
        if found_packages:
            print("Found packages:")
            for pkg in found_packages:
                print(f"- {pkg}: {self.available_packages[pkg]}")
        else:
            print("No packages found.")

    def list_package_info(self, package_name):
        if package_name in self.available_packages:
            print(f"Package: {package_name}")
            print(f"Description: {self.available_packages[package_name]}")
            # Здесь можно добавить логику для отображения зависимостей
        else:
            print(f"Package '{package_name}' not found.")


    def install_package(self, package_name):
        if package_name in self.available_packages:
            if package_name not in self.installed_packages:
                print(f"Starting installation of '{package_name}'...")
                # Симуляция процесса установки
                total_steps = 10  # Общее количество шагов для установки
                for step in range(total_steps + 1):
                    time.sleep(0.5)  # Симуляция времени установки
                    percent = (step / total_steps) * 100
                    bar_length = 40  # Длина полоски
                    block = int(round(bar_length * step / total_steps))
                    progress = "#" * block + "-" * (bar_length - block)
                    print(f"\r[{progress}] {percent:.2f}%", end='')

                print(f"\nPackage '{package_name}' installed successfully.")
                self.installed_packages.append(package_name)
                self.save_installed_packages()
            else:
                print(f"Package '{package_name}' is already installed.")
        else:
            print(f"Package '{package_name}' not found in available packages.")


    def list_installed_packages(self):
        if self.installed_packages:
            print("Installed packages:")
            for pkg in self.installed_packages:
                print(f"- {pkg}: {self.available_packages[pkg]}")
        else:
            print("No packages installed.")

    def list_available_packages(self):
        print("Available packages:")
        for pkg, desc in self.available_packages.items():
            if pkg not in self.installed_packages:
                print(f"- {pkg}: {desc}")


    def run_my_nano(self, filename):
        nano_script = os.path.join(self.base_directory, "bin", "my_nano.py")
        os.system(f"python {nano_script} {filename}")

    def run_snake_game(self):
        snake_script = os.path.join(self.base_directory, "bin", "snakegame.py")
        os.system(f"python {snake_script}")

    def run_browser(self):
        browser_script = os.path.join(self.base_directory, "bin", "browser.py")
        os.system(f"python {browser_script}")

    def run_echo(self):
        echo_script = os.path.join(self.base_directory, "bin", "echo.py")
        os.system(f"python {echo_script}")

    def download_file(self, url):
        try:
            filename = url.split("/")[-1]  # Получаем имя файла из URL
            file_path = os.path.join(self.current_directory, filename)

            # Получаем размер файла
            with urllib.request.urlopen(url) as response:
                total_size = int(response.getheader('Content-Length', 0))
                downloaded_size = 0

                with open(file_path, 'wb') as out_file:
                    while True:
                        data = response.read(1024)  # Читаем данные порциями по 1 КБ
                        if not data:
                            break
                        out_file.write(data)
                        downloaded_size += len(data)

                        # Вычисляем процент загрузки
                        percent = (downloaded_size / total_size) * 100
                        bar_length = 40  # Длина полоски
                        block = int(round(bar_length * downloaded_size / total_size))
                        progress = "#" * block + "-" * (bar_length - block)
                        print(f"\r[{progress}] {percent:.2f}%", end='')

            print(f"\nFile '{filename}' downloaded successfully to {self.current_directory}.")
        except Exception as e:
            print(f"Error downloading file: {e}")


    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_system_info(self):
        print("System Information:")
        print("OS: Amaterasu Bullnix 1.0.2")
        print("Kernel: 1.1.0")
        print("Installed Packages:")
        for pkg in self.installed_packages:
            print(f"- {pkg}")
        print("sh: akaish")

    def clone_repository(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        destination_path = os.path.join(self.home_directory, repo_name)

        if os.path.exists(destination_path):
            print(f"Repository '{repo_name}' already exists in {self.home_directory}.")
            return

        try:
            os.system(f"git clone {repo_url} {destination_path}")
            print(f"Repository '{repo_name}' cloned successfully into {self.home_directory}.")
        except Exception as e:
            print(f"Error cloning repository: {e}")

    def check_permissions(self, file_path, action):
        """Проверка прав доступа к файлу."""
        if self.username == "toor" or self.username in self.sudoers:
            return True  # Пользователь toor всегда имеет доступ ко всем файлам

        if file_path in self.file_permissions:
            permissions = self.file_permissions[file_path]
            if action == "read":
                return permissions["read"]
            elif action == "write":
                return permissions["write"] and permissions["owner"] == self.username
        return False
        
    def execute_dosu_command(self, command):
        if self.username == "toor" or self.username in self.sudoers:
            print(f"Executing")
            print(f"Executing command with admin privileges: {command}")
            self.execute_command(command)  # Выполняем команду с полными правами
        else:
            print("You do not have permission to use 'dosu'.")
            
    def cat_file(self, filename):
        file_path = os.path.join(self.current_directory, filename)
        
        if not os.path.exists(file_path):
            print(f"File '{filename}' does not exist.")
            return
        
        if not self.check_permissions(file_path, "read"):
            print(f"You do not have permission to read '{filename}'.")
            return
        
        with open(file_path, "r") as f:
            content = f.read()
            print(content)  # Выводим содержимое файла

    
    def run_guess_number_game(self):
        game_script = os.path.join(self.base_directory, "bin", "guess_number.py")
        os.system(f"python {game_script}")

    def runpy(self):
        runpy_script = os.path.join(self.base_directory, "bin", "runpy.py")
        os.system(f"python {runpy_script}")

    def xorgstart(self):
        xstart_script = os.path.join(self.base_directory, "bin", "windowmaker.py")
        os.system(f"python {xstart_script}")

    def fdisk(self):
        fdisk_script = os.path.join(self.base_directory, "bin", "fdisk.py")
        os.system(f"python {fdisk_script}")

    def kitkat(self, sub_command):
        kitkat_script = os.path.join(self.base_directory, "bin", "kitkat.py")

        # Разделяем подкоманду и пакет
        parts = sub_command.split()

        if len(parts) < 1:
            print("Ошибка: необходимо указать команду.")
            return

        command = parts[0]
        package = parts[1] if len(parts) > 1 else None  # Устанавливаем package в None, если его нет

        try:
            # Запускаем kitkat.py с аргументами командной строки
            if package:
                result = subprocess.run(['python', kitkat_script, command, package], check=True, text=True, capture_output=True)
            else:
                result = subprocess.run(['python', kitkat_script, command], check=True, text=True, capture_output=True)

            print(result.stdout)  # Выводим стандартный вывод скрипта
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении kitkat.py: {e.stderr}")  # Выводим ошибку, если скрипт завершился с ошибкой

if __name__ == "__main__":
    game_os = amaterasu()
    game_os.run()
