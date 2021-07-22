from math import log2
import string
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


class StrengthSizer(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.strengthbar = PWStrengthIndicator(self)
        self.label = StaticText(self, label="Password strength:")
        self.strength_label = StaticText(self)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer.Add(self.label, 1, wx.ALIGN_TOP)
        self.hsizer.Add(self.FromDIP(wx.Size(40, 20)))
        self.vsizer.Add(self.strengthbar, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.vsizer.Add(self.strength_label, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.hsizer.Add(self.vsizer, 1, wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.hsizer)


class PWStrengthIndicator(wx.Panel):
    def __init__(self, parent, password=None):
        super().__init__(parent)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.min_size = self.FromDIP(wx.Size(100, 21))
        self.bar_size = self.FromDIP(wx.Size(100, 10))
        self.SetMinSize(self.min_size)
        coords = self.FromDIP(wx.Size(5, 6))
        radius = self.FromDIP(wx.Size(5, 4))
        self.radius = radius[1]
        self.ycoord = coords[1]
        if password:
            self.password = password

    def set_pw(self, password):
        self.password = password

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        if self.password:
            strength = self.calc_strength()
            colour = self.setcolourandlabel(strength)
            update = self.FromDIP(wx.Size(strength, 10))
            dc.SetBrush(wx.Brush(grey_btn))
            dc.DrawRoundedRectangle(
                -1, self.ycoord, self.bar_size[0], self.bar_size[1], self.radius
            )
            dc.SetBrush(wx.Brush(colour))
            dc.DrawRoundedRectangle(
                -1, self.ycoord, update[0], self.bar_size[1], self.radius
            )

    def setcolourandlabel(self, strength):
        if strength <= 20:
            label = "Weak"
            colour = wx.Colour(255, 128, 128)
        if strength > 20 and strength <= 40:
            label = "Fair"
            colour = wx.Colour(240, 187, 112)
        if strength > 40 and strength <= 60:
            label = "Good"
            colour = wx.Colour(224, 214, 101)
        if strength > 60 and strength <= 80:
            label = "Very Good"
            colour = wx.Colour(104, 178, 114)
        if strength > 80:
            label = "Excellent"
            colour = wx.Colour(149, 255, 164)

        self.Parent.strength_label.SetLabel(label)
        self.Parent.vsizer.Layout()
        return colour

    def calc_strength(self):
        lowerc = list(string.ascii_lowercase)
        upperc = list(string.ascii_uppercase)
        digits = list(string.digits)
        symbols = list(string.punctuation)
        list_pw = list(self.password)
        length_pw = len(list_pw) + 1
        dict_pw = {i: f for i, f in enumerate(list_pw)}
        values = dict_pw.values()
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

        if pool_size != 0:
            entropy = length_pw * log2(pool_size)
            normalised_e = self.normalise_range(entropy)

        return normalised_e

    def check_contents(self, charset, values):
        for char in charset:
            if char in values:
                return True
        return False

    def normalise_range(self, entropy):
        max_entropy = 217
        max_normalised = 100
        slope = max_normalised / max_entropy
        normalised = slope * entropy
        return round(normalised)


class DBpanel(wx.Panel):
    def __init__(self, parent, db=None):
        super().__init__(parent)
        self.db = db


class StaticText(wx.StaticText):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.SetForegroundColour(off_white)
