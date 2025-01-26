import curses
from random import randint

# Настройка окна
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()  # Получаем размеры окна
w = curses.newwin(sh, sw, 0, 0)  # Создаем новое окно
w.keypad(1)  # Включаем поддержку клавиш
w.timeout(100)  # Устанавливаем таймаут

# Начальные параметры змейки
snk_x = sw // 4
snk_y = sh // 2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]
food = [sh // 2, sw // 2]  # Начальная позиция яблока
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)  # Отображаем яблоко

key = curses.KEY_RIGHT  # Начальное направление

while True:
    next_key = w.getch()  # Получаем нажатую клавишу
    key = key if next_key == -1 else next_key  # Если клавиша не нажата, сохраняем текущее направление

    # Вычисляем новое положение головы змейки
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Проверка на столкновение со стенами или с самой собой
    if (new_head[0] in [0, sh] or
            new_head[1] in [0, sw] or
            new_head in snake):
        curses.endwin()
        quit()

    # Добавляем новую голову змейки
    snake.insert(0, new_head)

    # Проверка на съеденное яблоко
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                randint(1, sh - 1),
                randint(1, sw - 1)
            ]
            food = nf if nf not in snake else None
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    else:
        # Удаляем последний сегмент змейки
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Отображаем змейку
    w.addch(int(snake[0][0]), int(snake[0][1]), '#')

