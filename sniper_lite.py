import math
import win32gui
import win32api
import pynput
import PySimpleGUI as sg
from threading import Thread
from ddtank import Status
from ddtank.utils.aim import operate_calculate_strength
from typing import Optional

from utils import is_game

layout = [
    [sg.Text('Suggestion: ', key='text-suggestion', background_color='white', font=('Times NewRoman', 12), text_color='black')],
]

menu_def = [
    [],
    ['&Exit']
]

window = sg.Window(
    'ddtankSniper',
    layout,
    keep_on_top=True,
    location=(0, 0),
    no_titlebar=True,
    grab_anywhere=True,
    alpha_channel=0.7,
    margins=(0, 0),
    background_color='white',
    right_click_menu=menu_def
)

old_handle: int = 0
game: Optional[Status] = None
sniper: bool = False


def listen():
    def on_press(key):
        global sniper
        if key == pynput.keyboard.Key.ctrl_l:
            sniper = True

    def on_release(key):
        global sniper
        if key == pynput.keyboard.Key.ctrl_l:
            sniper = False

    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener:
        key_listener.join()


listen_thread = Thread(target=listen)
listen_thread.setDaemon(True)
listen_thread.start()

while True:
    event, values = window.read(timeout=100)
    if event in (None, 'Exit'):
        exit()
    else:
        handle = win32gui.GetForegroundWindow()
        if handle != old_handle:
            old_handle = handle
            game_handle = is_game(handle)
            if game_handle:
                title = win32gui.GetWindowText(handle)
                game = Status(game_handle)
            else:
                game = None
                window['text-suggestion'].update('Suggestion: None')
        if game:
            mouse_pos, game_pos = win32api.GetCursorPos(), win32gui.GetWindowRect(game.handle)
            pos = ((mouse_pos[0] - game_pos[0]) / 1000, (mouse_pos[1] - game_pos[1]) / 600)
            if game.find('find', pos=(510, 169), rgb=(222, 194, 106)):
                game.read()
                if sniper and 0 < pos[0] < 1 and 0 < pos[1] < 1 and game.circle:
                    x = game.box_pos[0] + pos[0] * game.box_width * 10
                    y = game.box_pos[1] + pos[1] * game.box_width * 6
                    distance = ((x - game.circle[0]) / game.box_width, -(y - game.circle[1]) / game.box_width)
                    strength = operate_calculate_strength(
                        game.angle,
                        game.wind * math.copysign(1, distance[0]),
                        abs(distance[0]),
                        distance[1]
                    )
                    window['text-suggestion'].update(f'Suggestion: {strength:.1f}')
                else:
                    window['text-suggestion'].update('Suggestion: None')
