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
    
    def exit(self):
        confirm = input("Are you sure you want to exit? (y/n): ")
        if confirm.lower() == 'y':
            print("Exiting from Amaterasu Bullnix...")
            sys.exit(0)

    def run(self):
        print("Welcome to Amaterasu Bullnix")
        while True:
            # Заменяем домашнюю директорию на ~ в приглашении
            if self.current_directory == self.home_directory:
                current_dir_display = "~"
            else:
                current_dir_display = self.current_directory.replace(self.home_directory, "~")

            prompt = f"{self.username}@amaterasu:{current_dir_display}# " if self.username == "toor" else f"{self.username}@amaterasu:{current_dir_display}$ "
            command = input(prompt)
            self.execute_command(command)

    def load_commands(self):
        with open('commands.json', 'r') as f:
            self.commands = json.load(f)['commands']

    def load_installed_packages(self):
        packages_dir = os.path.join(self.base_directory, 'bin')  # Путь к директории с пакетами
        packages = []

        # Проверяем, существует ли директория
        if os.path.exists(packages_dir):
            # Проходим по всем файлам в директории
            for filename in os.listdir(packages_dir):
                # Проверяем, является ли файл Python
                if filename.endswith('.py'):
                    packages.append(filename[:-3])  # Добавляем имя файла без .py

        return packages


    def execute_command(self, command):
        # Split the command into name and arguments
        parts = command.split()
        cmd_name = parts[0]
        args = parts[1:]

        # Dictionary with commands and usage messages
        usage_messages = {
            'cd': "Usage: cd <directory>",
            'makedir': "Usage: makedir <directory>",
            'rm': "Usage: rm <filename>",
            'mv': "Usage: mv <source> <destination>",
            'wget': "Usage: wget <url>",
            'git': "Usage: git <repository_url>",
            'ls': "Usage: ls",
            'clear': "Usage: clear",
            'myfetch': "Usage: myfetch",
            'dosu': "Usage: dosu <command>",
            'exit': "Usage: exit",  # Add exit command usage
            # Add other commands as needed
        }

        # List of non-bin commands
        non_bin_commands = list(usage_messages.keys())

        if cmd_name in non_bin_commands:
            if cmd_name == 'exit':
                self.exit()  # Call the exit method directly
                return

            method = getattr(self, cmd_name, None)
            if method:
                # Check if an argument is required for the command
                if cmd_name in usage_messages and (len(args) == 0 and cmd_name != 'ls' and cmd_name != 'clear' and cmd_name != 'myfetch'):
                    print(usage_messages[cmd_name])
                else:
                    method(*args)
            else:
                print("Unknown command")
            return

        # If the command is not in the list, check if it is a Python file in bin
        python_file_path = os.path.join(self.base_directory, 'bin', f"{cmd_name}.py")
        if os.path.isfile(python_file_path):
            try:
                subprocess.run(['python', python_file_path] + args)
            except Exception as e:
                print(f"Error running {cmd_name}: {e}")
        else:
            print("Unknown command")


        
    def cd(self, dirname):
        new_directory = os.path.join(self.current_directory, dirname)

        if not dirname:
            print("Usage: cd <directory>")
            return
        
        if dirname == "..":
            new_directory = os.path.dirname(self.current_directory)
        elif os.path.isabs(dirname):
            new_directory = dirname

        if os.path.isdir(new_directory):
            self.current_directory = new_directory
            print(f"Changed directory to: {self.current_directory}")
        else:
            print(f"Directory '{dirname}' not found.")

    def makedir(self, dirname):
        dir_path = os.path.join(self.current_directory, dirname)
        try:
            os.makedirs(dir_path, exist_ok=False)
            self.file_permissions[dirname] = {"owner": self.username, "read": True, "write": True}
            print(f"Directory '{dirname}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dirname}' already exists.")

    def rm(self, filename):
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

    def mv(self, src, dest):
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

    def ls(self):
        print("Contents of the current directory:")
        for item in os.listdir(self.current_directory):
            print(f"- {item}")

    def wget(self, url):
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


    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def myfetch(self):
        ascii_art = """
                      XXX                 
                      X                   
                     X             XX     
     XXX          XXXXXXXXX     XXX       
        XX     XXXXXXXXXXXXX  X X         
           X XXXXXXXX  XXXXXXXX           
              XXXXXX    XXXXXX            
             XXXXXX  XX  XXXXXX           
             XXXXX  XXXX  XXXXXXXXX       
      XX X  XXXXX          XXXX    X  X   
    XX        XX  XXXXXXXX  XXX        XXX
                 XXXXXXXXXXX              
                X XXXXXXXXXX  X           
             XX        X       X          
            X          X        X         
                      X           X       
                     XX           XX      
                     X                    
        """
        print(ascii_art)
        print("System Information:")
        print("-------------------")
        print("OS: Amaterasu Bullnix 1.2.0")
        print("Kernel: 1.1.0")
        print("------------------")
        print("sh: akaish")


    def git(self, repo_url):
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
        
    def dosu(self, command):
        if self.username == "toor" or self.username in self.sudoers:
            print(f"Executing")
            print(f"Executing command with admin privileges: {command}")
            self.execute_command(command)  # Выполняем команду с полными правами
        else:
            print("You do not have permission to use 'dosu'.")
            
    def cat(self, filename):
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


if __name__ == "__main__":
    game_os = amaterasu()
    game_os.run()
