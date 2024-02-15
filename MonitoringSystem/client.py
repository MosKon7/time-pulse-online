import ctypes
import sys

from pystray import MenuItem as item
from pystray import Icon as icon, Menu as menu
from PIL import Image

import webbrowser

import time
import pyautogui
import keyboard
import requests
import threading
import socket

# URL сервера, куда будут отправляться данные
#server_url = 'https://ваш_сервер/путь_к_обработчику'

# Имя системы сотрудника
USER = socket.gethostname()
# Интервал отправки данных в секундах (10 минут - 600)
INTERVAL = 10
# Переменные для отслеживания нажатий клавиш
KEY_PRESS_COUNT = 0
# Глобальная переменная для управления состоянием работы
STATE = 0

# Свойства иконки в трее
TRAY_TOOLTIP = 'MonitoringSystem'
TRAY_ICON = 'icon.ico'

# Патерны сообщений
MASS_STATE_START = "Начало рабочего дня"
MASS_STATE_PAUSE = "Перерыв"
MASS_STATE_STOP = "Конец рабочего дня"



# ВЗАИМОДЕЙСТВИЯ С ОКНОМ И СОСТОЯНИЕМ
# Функция, которая будет вызываться при изменении переменной STATE
def on_state_change(icon, state):
    global STATE
    if STATE != state:
        STATE = state
        if 1:
            icon.notify(MASS_STATE_START)
        elif 2:
            icon.notify(MASS_STATE_PAUSE)
        elif 0:
            icon.notify(MASS_STATE_STOP)


def open_website(icon, url):
    webbrowser.open(url)


# Создаем пункты подменю для "Рабочего дня"
# заполняем массивом задач полученных с сервера.
workday_submenu = menu(item(MASS_STATE_START, lambda icon, item: on_state_change(icon, 1)),
                 item(MASS_STATE_PAUSE, lambda icon, item: on_state_change(icon, 2)),
                 item(MASS_STATE_STOP, lambda icon, item: on_state_change(icon, 0)))
workday_menu = item('Рабочий день', workday_submenu)

# Создаем пункты подменю для "Задач"
# заполняем массивом задач полученных с сервера.
tasks_submenu = menu(item('Задача 1', lambda icon, item: open_website(icon, "https://www.example1.com/task?1")),
                 item('Задача 2', lambda icon, item: open_website(icon, "https://www.example2.com/task?2")),
                 item('Задача 3', lambda icon, item: open_website(icon, "https://www.example3.com/task?3")))
tasks_menu = item('Задачи на день', tasks_submenu)

# Создаем иконку в трее
def create_tray_icon():
    image = Image.open(TRAY_ICON)  # Указываем путь к иконке
    # Пункты в контекстное меню
    menu_items = [
        workday_menu,
        tasks_menu,
        item('Статистика', lambda icon, item: open_website(icon, "https://www.example3.com/statistic/"))
    ] 

    menu_popup = menu(*menu_items)

    tray_icon = icon(TRAY_TOOLTIP, image, menu=menu_popup)

    print(tray_icon.menu.items[0])
    return tray_icon

def open_website(icon, url):
    webbrowser.open(url)
        


# МОНИТОРИНГ
# Функция для отслеживания нажатий клавиш в отдельном потоке
# Однакратное нажатие клавиши считается за 2, тк происходит непосредственно нгажатие и отпускание клавиши
def track_keys():
    global KEY_PRESS_COUNT
    keyboard.hook(lambda e: on_key_press(e))
    keyboard.wait(INTERVAL)
    keyboard.unhook_all()
    
# Функция обработки нажатий клавиш
def on_key_press(event):
    global KEY_PRESS_COUNT
    KEY_PRESS_COUNT += 1




# ОСНОВНАЯ ФУНКЦИЯ
# Функция для отслеживания активности в отдельном потоке
def track_activity():
    # Скрываем консольное окно
    #hide_console_window()
    
    global KEY_PRESS_COUNT
    global STATE
    
    while True:
        try:
            if STATE > 0:
                # Получаем текущее время
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')

                # Получаем координаты мыши
                mouse_position = pyautogui.position()

                # Формируем данные для отправки на сервер
                data = {
                    'timestamp': current_time,
                    'state': STATE,
                    'key_press_count': KEY_PRESS_COUNT,
                    'mouse_x': mouse_position[0],
                    'mouse_y': mouse_position[1]
                }

                # Сбрасываем счетчик нажатий клавиш
                KEY_PRESS_COUNT = 0

                # Отправляем данные на сервер
                #response = requests.post(server_url, json=data)

                # Выводим статус код ответа
                #print(f'Status Code: {response.status_code}')
                print(f'Отправляемые данные: {data}')
            else: 
                print(f'Офлайн')
                
        except Exception as e:
            print(f'Error: {e}')

        # Ждем до следующего интервала
        time.sleep(INTERVAL)



# ОБРАБОТКА ПОТОКОВ  

# Создаем и запускаем поток для отслеживания нажатий клавиш
keys_thread = threading.Thread(target=track_keys)
keys_thread.start()

# Создаем и запускаем поток для отслеживания активности
activity_thread = threading.Thread(target=track_activity)
activity_thread.start()

# Создаем иконку в трее
tray_icon = create_tray_icon()
# Создаем и запускаем поток для иконки в трее
tray_thread = threading.Thread(target=tray_icon.run())
tray_thread.start()

# Главный поток программы может продолжать выполнять другие задачи
while True:
    time.sleep(1)