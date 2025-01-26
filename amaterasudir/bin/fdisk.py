import psutil

def list_partitions():
    print("Список разделов:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Точка монтирования: {partition.mountpoint}")
        print(f"Файловая система: {partition.fstype}")
        print(f"Опции: {partition.opts}")
        print("-" * 40)

def main():
    print("Утилита для работы с дисками")
    while True:
        print("1. Показать разделы")
        print("2. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            list_partitions()
        elif choice == '2':
            print("Выход из утилиты.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()

