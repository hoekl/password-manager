from pynput import keyboard
import threading
import subprocess


def on_quit():
    exit()


def start_gui():
    subprocess.call(["pythonw.exe", "GUI.py"])


def thread_start():
    th = threading.Thread(target=start_gui)
    th.start()


with keyboard.GlobalHotKeys({"<ctrl>+c": on_quit, "<alt>+w": thread_start}) as h:
    h.join()
