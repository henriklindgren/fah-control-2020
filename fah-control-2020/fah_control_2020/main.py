import PySimpleGUI
from fah_control_2020.ui import FAHWindow

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


if __name__ == '__main__':
    PySimpleGUI.ChangeLookAndFeel('Material2')
    with FAHWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT) as fah_window:
        fah_window.run()
