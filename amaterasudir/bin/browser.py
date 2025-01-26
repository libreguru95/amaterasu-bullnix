import requests
from bs4 import BeautifulSoup
import curses
from PIL import Image
import numpy as np
from io import BytesIO

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return str(e)

def fetch_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        return None

def image_to_ascii(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 для корректировки высоты
    image = image.resize((new_width, new_height))
    image = image.convert("L")  # Преобразование в градации серого
    pixels = np.array(image)
    chars = np.array(list(" .:-=+*%@#"))  # Символы для отображения
    ascii_image = chars[(pixels // 25.5).astype(int)]  # Преобразование пикселей в символы
    return "\n".join("".join(row) for row in ascii_image)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    url = "http://example.com"  # Замените на нужный URL
    history = [url]
    current_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Текущий URL: {url}")
        stdscr.addstr(1, 0, "Нажмите 'g' для перехода по URL, 'b' для назад, 'q' для выхода.")
        
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Получаем первое изображение на странице
        image_url = None
        for img in soup.find_all('img', src=True):
            image_url = img['src']
            if not image_url.startswith('http'):
                image_url = url + image_url  # Преобразуем относительный путь в абсолютный
            break  # Берем только первое изображение

        if image_url:
            image = fetch_image(image_url)
            if image:
                ascii_image = image_to_ascii(image)
            else:
                ascii_image = "Не удалось загрузить изображение."
        else:
            ascii_image = "Изображение не найдено."

        # Проверка размера ASCII-арта перед отображением
        ascii_lines = ascii_image.splitlines()
        max_height = curses.LINES - 4  # Оставляем место для других строк
        if len(ascii_lines) > max_height:
            ascii_image = "\n".join(ascii_lines[:max_height])  # Ограничиваем количество строк

        stdscr.addstr(3, 0, ascii_image)

        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('g'):
            stdscr.clear()
            stdscr.addstr(0, 0, "Введите URL: ")
            curses.echo()
            url = stdscr.getstr(0, 15, 100).decode('utf-8')
            history.append(url)
            current_index += 1
            curses.noecho()
        elif key == ord('b') and current_index > 0:
            current_index -= 1
            url = history[current_index]
        elif key == ord('q'):
            break

curses.wrapper(main)
