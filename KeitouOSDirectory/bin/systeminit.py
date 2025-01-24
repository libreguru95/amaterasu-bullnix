import time
import random
import sys

def simulate_service_start(service_name):
    # Симуляция прогресса
    for i in range(101):
        time.sleep(0.005)  # Задержка для имитации времени загрузки
        # Вывод прогресса
        sys.stdout.write(f"\rStarting service {service_name} [{'#' * (i // 2)}{' ' * (50 - i // 2)}] - {i}%")
        sys.stdout.flush()
    print()  # Переход на новую строку после завершения

def main():
    services = [
        "httpd",
        "sshd",
        "cron",
        "nginx",
        "mysql",
        "postgresql",
        "redis",
        "docker",
        "networking",
        "firewalld",
        "ntpd",
        "syslog",
        "bluetooth",
        "cups",
        "avahi-daemon",
        "rsyslog",
        "ssh-agent",
        "gdm",
        "lightdm",
        "xrdp"
    ]

    print("Welcome to KeitouOS, Starting System...")
    print()

    for service in services:
        simulate_service_start(service)

    print("All services started successfully!")

if __name__ == "__main__":
    main()
