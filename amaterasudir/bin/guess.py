import random

def play_guess_number():
    print("Добро пожаловать в игру 'Угадай число'!")
    print("Я загадал число от 1 до 100. Попробуйте угадать его!")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("Введите ваше предположение: "))
            attempts += 1

            if guess < secret_number:
                print("Слишком низко! Попробуйте еще раз.")
            elif guess > secret_number:
                print("Слишком высоко! Попробуйте еще раз.")
            else:
                print(f"Поздравляю! Вы угадали число {secret_number} за {attempts} попыток.")
                break
        except ValueError:
            print("Пожалуйста, введите корректное число.")

if __name__ == "__main__":
    play_guess_number()

