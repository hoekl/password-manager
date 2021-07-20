import wx

grey_btn = wx.Colour(69, 69, 69)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(55, 55, 55)
edit_colour = wx.Colour(63, 63, 63)


class Button(wx.Button):
    def __init__(self, parent, label=None, **kw):
        super().__init__(parent, label=label, style=wx.BORDER_NONE, **kw)
        self.SetBackgroundColour(grey_btn)
        self.SetForegroundColour(off_white)
        self.SetLabel(label)
        if kw:
            self.SetName(kw["name"])

class TextCtrl(wx.TextCtrl):
    def __init__(self, parent, style=wx.TE_READONLY | wx.BORDER_SIMPLE, **kw):
        super().__init__(parent, style=style, **kw)
        self.SetForegroundColour(off_white)
        self.SetBackgroundColour(light_grey)
        if kw:
            try:
                self.SetName(kw["name"])
                self.SetValue(kw["value"])
            except Exception:
                pass

    def set_size(self):
        self.SetMaxSize(self.FromDIP(wx.Size(500, -1)))
        self.SetMinSize(self.FromDIP(wx.Size(300, -1)))

    def make_editable(self):
        self.SetBackgroundColour(edit_colour)
        self.SetEditable(True)

    def make_readonly(self):
        self.SetBackgroundColour(light_grey)
        self.SetEditable(False)


class PasswordCtrl(TextCtrl):
    def __init__(
        self,
        parent,
        value="abcdefg",
        style=wx.TE_READONLY | wx.TE_PASSWORD | wx.BORDER_SIMPLE,
        name="password",
    ):
        super().__init__(parent, value=value, style=style, name=name)

class DBpanel(wx.Panel):
    def __init__(self, parent, db=None):
        super().__init__(parent)
        self.db = db


class StaticText(wx.StaticText):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.SetForegroundColour(off_white)
