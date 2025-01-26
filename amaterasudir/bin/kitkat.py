import os
import requests
import argparse
import sys
import time

REPO_URL = "https://raw.githubusercontent.com/libreguru95/aur/main"  # URL to access files
API_URL = "https://api.github.com/repos/libreguru95/aur/contents"  # URL to access the API
TARGET_DIRECTORY = "amaterasudir/usr"

def ensure_target_directory():
    """Creates the target directory if it does not exist."""
    os.makedirs(TARGET_DIRECTORY, exist_ok=True)

def download_package(package_name):
    target_path = os.path.join(TARGET_DIRECTORY, f"{package_name}.py")
    
    # Remove the old version if it exists
    if os.path.exists(target_path):
        os.remove(target_path)
    
    # Form the URL to download the file
    file_url = f"{REPO_URL}/{package_name}.py"
    
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Check that the request was successful
        
        # Get the total file size for the progress indicator
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # Save the file to the target directory with a progress indicator
        with open(target_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                downloaded_size += len(data)
                # Update the progress indicator
                progress = downloaded_size / total_size * 100
                print(f"\rDownloading {package_name}: [{'#' * int(progress // 2):<50}] - {progress:.2f}%", end="")
        
        print()  # Move to a new line after the download is complete
        print(f"Package {package_name} has been successfully installed.")
    except requests.HTTPError:
        print(f"Package {package_name} not found in the repository.")
    except Exception as e:
        print(f"An error occurred while downloading the package: {e}")

def update_package(package_name):
    target_path = os.path.join(TARGET_DIRECTORY, f"{package_name}.py")
    
    if os.path.exists(target_path):
        download_package(package_name)  # Simply reload the file
    else:
        print(f"Package {package_name} is not installed. Install it using the command 'kitkat install {package_name}'.")

def list_packages():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check that the request was successful
        
        packages = [item['name'] for item in response.json() if item['name'].endswith('.py')]
        
        if packages:
            print("Available packages:")
            for package in packages:
                print(f" - {package[:-3]}")  # Remove .py from the name
        else:
            print("No available packages.")
    except Exception as e:
        print(f"An error occurred while retrieving the list of packages: {e}")

def update_all_packages():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check that the request was successful
        
        packages = [item['name'] for item in response.json() if item['name'].endswith('.py')]
        
        if packages:
            print("Updating all packages...")
            for package in packages:
                update_package(package[:-3])  # Remove .py from the name
        else:
            print("No available packages for update.")
    except Exception as e:
        print(f"An error occurred while retrieving the list of packages: {e}")

def main():
    ensure_target_directory()  # Ensure the target directory exists

    parser = argparse.ArgumentParser(description='KitKat package manager for KeitouOS, This is version for Amaterasu Bullnix')
    parser.add_argument('command', choices=['install', 'update', 'list', 'update-all'], help='Command to execute')
    parser.add_argument('package', nargs='?', help='Package name (without .py)')

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
