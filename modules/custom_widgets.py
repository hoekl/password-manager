import wx
grey_btn = wx.Colour(69, 69, 69)
off_white = wx.Colour(235, 235, 235)

class Button(wx.Button):
    def __init__(self, parent, label=None, style=wx.BORDER_NONE, **kw):
        super().__init__(parent, label=label, style=wx.BORDER_NONE, **kw)
        self.SetBackgroundColour(grey_btn)
        self.SetForegroundColour(off_white)
        self.SetLabel(label)
        if kw:
            self.SetName(kw["name"])

    def setName(self, name):
        self.SetName(name)
