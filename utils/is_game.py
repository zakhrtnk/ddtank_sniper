import win32gui
from typing import Optional

def is_game(handle: int) -> Optional[int]:
    child_hwnd_list = []
    win32gui.EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd), child_hwnd_list)
    for child_hwnd in child_hwnd_list:
        class_name, shape = win32gui.GetClassName(child_hwnd), win32gui.GetWindowRect(child_hwnd)
        height = shape[3] - shape[1]
        weight = shape[2] - shape[0]
        if class_name == 'MacromediaFlashPlayerActiveX' and weight == 1000 and height == 600:
            return child_hwnd
    else:
        return None

