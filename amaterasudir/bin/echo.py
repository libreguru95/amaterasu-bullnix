# echo.py

def main():
    print("Введите текст (введите 'exit' для выхода):")
    while True:
        user_input = input("> ")  # Запрашиваем ввод от пользователя
        if user_input.lower() == 'exit':  # Проверяем, не ввел ли пользователь 'exit'
            print("Выход из программы.")
            break
        print(f"Вы ввели: {user_input}")  # Выводим введенный текст

if __name__ == "__main__":
    main()

