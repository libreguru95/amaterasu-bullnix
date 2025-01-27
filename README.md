# Amaterasu Bullnix
This is a fork of KeitouOS, the purpose of this distribution is to improve the operating system simulator by changing the main code.
Sure! Here’s the documentation translated into English:

---

# Amaterasu Bullnix - Documentation

## Description
Amaterasu Bullnix is a simple command shell written in Python that allows users to interact with the file system, execute commands, and manage files. The shell supports a permission system and provides basic commands for working with files and directories.

## Classes

### 1. SystemInit
Class for system initialization.

#### Attributes:
- **base_directory (str)**: The base directory for system initialization.

#### Methods:
- **run_systeminit()**: Executes the system initialization script.

---

### 2. Amaterasu
Class for implementing the Amaterasu Bullnix command shell.

#### Attributes:
- **base_directory (str)**: The base directory for the system.
- **username (str)**: The username.
- **home_directory (str)**: The user's home directory.
- **current_directory (str)**: The current directory.
- **installed_packages (list)**: A list of installed packages.
- **color_scheme (str)**: The color scheme of the interface.
- **file_permissions (dict)**: The file access permission system.
- **sudoers (list)**: A list of users with sudo rights.
- **commands (dict)**: Loaded commands from the commands.json file.

#### Methods:
- **create_home_directory()**: Creates the user's home directory.
- **create_directory_structure()**: Creates the directory structure.
- **load_username()**: Loads the username from a file or prompts for it.
- **load_sudoers()**: Loads the list of users with sudo rights.
- **exit()**: Exits the program.
- **run()**: Starts the main command shell loop.
- **load_commands()**: Loads commands from the commands.json file.
- **load_installed_packages()**: Loads the list of installed packages.
- **execute_command(command)**: Executes the entered command.
- **cd(dirname)**: Changes the current directory.
- **makedir(dirname)**: Creates a new directory.
- **rm(filename)**: Deletes a file.
- **mv(src, dest)**: Moves a file or directory.
- **ls()**: Displays the contents of the current directory.
- **wget(url)**: Downloads a file from the specified URL.
- **clear()**: Clears the screen.
- **myfetch()**: Displays system information.
- **git(repo_url)**: Clones a Git repository.
- **check_permissions(file_path, action)**: Checks file access permissions.
- **dosu(command)**: Executes a command with administrator privileges.
- **cat(filename)**: Displays the contents of a file.

## Installation and Usage
1. Download or clone the repository.
2. Ensure you have Python installed.
3. Run the `main.py` file to start using the shell.

## Notes
- The shell supports basic commands such as `cd`, `ls`, `mkdir`, `rm`, `mv`, `wget`, and others.
- The user `toor` has full access rights to all commands and files.
- To execute commands with administrator privileges, use the `dosu` command.

---
