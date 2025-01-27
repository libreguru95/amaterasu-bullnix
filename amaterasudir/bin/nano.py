import curses

def main(stdscr):
    # Очищаем экран
    stdscr.clear()
    
    # Устанавливаем режим ввода
    curses.cbreak()
    stdscr.keypad(True)
    
    # Инициализируем переменные
    text = [""]
    current_line = 0
    current_col = 0

    while True:
        # Отображаем текст
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()  # Получаем размеры окна
        for i, line in enumerate(text):
            if i < max_y - 3:  # Оставляем место для справки
                stdscr.addstr(i, 0, line)
        
        # Отображаем справку
        stdscr.addstr(max_y - 23, 0, "Горячие клавиши:")
        stdscr.addstr(max_y - 22, 0, "  Ctrl+S - Сохранить файл")
        stdscr.addstr(max_y - 21, 0, "  Esc - Выйти")
        
        # Перемещаем курсор
        stdscr.move(current_line, current_col)

        # Получаем ввод пользователя
        key = stdscr.getch()

        if key == curses.KEY_UP and current_line > 0:
            current_line -= 1
            current_col = min(current_col, len(text[current_line]))
        elif key == curses.KEY_DOWN and current_line < len(text) - 1:
            current_line += 1
            current_col = min(current_col, len(text[current_line]))
        elif key == curses.KEY_LEFT and current_col > 0:
            current_col -= 1
        elif key == curses.KEY_RIGHT and current_col < len(text[current_line]):
            current_col += 1
        elif key == curses.KEY_BACKSPACE or key == 127:
            if current_col > 0:
                text[current_line] = text[current_line][:current_col - 1] + text[current_line][current_col:]
                current_col -= 1
            elif current_line > 0:
                current_col = len(text[current_line - 1])
                text[current_line - 1] += text[current_line]
                del text[current_line]
                current_line -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Проверяем, не превышает ли current_line количество строк
            if current_line < len(text):
                text.insert(current_line + 1, text[current_line][current_col:])
                text[current_line] = text[current_line][:current_col]
            else:
                text.append("")  # Добавляем новую строку, если current_line выходит за пределы
            current_line += 1
            current_col = 0
        elif key == 27:  # ESC для выхода
            break
        elif key == curses.KEY_DC:  # Delete
            if current_col < len(text[current_line]):
                text[current_line] = text[current_line][:current_col] + text[current_line][current_col + 1:]
        elif key == 19:  # Ctrl+S для сохранения
            save_file(stdscr, text)
        else:
            # Добавляем символ в текст
            if current_line >= len(text):
                text.append("")
            text[current_line] = text[current_line][:current_col] + chr(key) + text[current_line][current_col:]
            current_col += 1

    # Выход из режима curses
    curses.endwin()

def save_file(stdscr, text):
    stdscr.clear()
    stdscr.addstr(0, 0, "Введите имя файла для сохранения:")
    stdscr.refresh()
    
    filename = ""
    current_col = 0

    while True:
        stdscr.addstr(1, 0, filename)
        stdscr.move(1, current_col)
        key = stdscr.getch()

        if key == curses.KEY_BACKSPACE or key == 127:
            if current_col > 0:
                filename = filename[:-1]
                current_col -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break
        else:
            filename += chr(key)
            current_col += 1

    with open(filename, 'w') as f:
        for line in text:
            f.write(line + '\n')

    stdscr.addstr(2, 0, f"Файл '{filename}' сохранен. Нажмите любую клавишу для продолжения...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
