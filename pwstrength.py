import wx
from modules.login_creator import PWGenWindow
import ctypes
import string
from math import log2
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

class base(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel = wx.Panel(self)
        pwgen = wx.Button(panel, label="Generator")
        pwgen.Bind(wx.EVT_BUTTON, self.on_generate)


    def on_generate(self, event):
        with PWGenWindow(self, title="Generate") as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                value = dialog.txt_ctrl.Value
                self.calc_strength(value)
                self.on_generate(event)

    def calc_strength(self, pw):
        print(pw)
        lowerc = list(string.ascii_lowercase)
        upperc = list(string.ascii_uppercase)
        digits = list(string.digits)
        symbols = list(string.punctuation)
        list_pw = list(pw)
        length_pw = len(list_pw) + 1
        dict_pw = {i:f for i, f in enumerate(list_pw)}
        values = dict_pw.values()
        print(dict_pw)
        lower_bool = self.check_contents(lowerc, values)
        upper_bool = self.check_contents(upperc, values)
        digits_bool = self.check_contents(digits, values)
        symbols_bool = self.check_contents(symbols, values)
        pool_size = 0
        if lower_bool == True:
            pool_size += 26
        if upper_bool == True:
            pool_size += 26
        if digits_bool == True:
            pool_size += 10
        if symbols_bool == True:
            pool_size += 32
        # E = L * log2(R) where L is length, R is the pool size

        entropy = length_pw * log2(pool_size)
        print(entropy)


    def check_contents(self, charset, values):
        for char in charset:
            if char in values:
                return True
        return False

if __name__ == "__main__":
    app = wx.App()
    frm = base(None)
    frm.Show()
    app.MainLoop()
