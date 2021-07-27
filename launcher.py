from pynput import keyboard
import threading
import subprocess

def function_1():
    exit()

def function_2():
    subprocess.call(["python", "GUI.py"])


def thread_start():
    th = threading.Thread(target=function_2)
    th.start()


with keyboard.GlobalHotKeys({
        '<ctrl>+c': function_1,
        '<alt>+w': thread_start}) as h:
    h.join()
