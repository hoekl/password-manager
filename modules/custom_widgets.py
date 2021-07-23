from math import log2
import string
import wx
import secrets
import re

grey_btn = wx.Colour(69, 69, 69)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(55, 55, 55)
edit_colour = wx.Colour(63, 63, 63)
black = wx.Colour(28, 28, 28)


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
    def __init__(self, parent, c_style=None):
        super().__init__(parent)
        if c_style:
            self.strengthbar = PWStrengthIndicator(self, c_style=True)
            self.label = StaticText(self, label="Password strength:", c_style=True)
            self.strength_label = StaticText(self, c_style=True)
        else:
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
    def __init__(self, parent, password=None, c_style=None):
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
        else:
            self.password = None
        if c_style:
            self.bgcolour = off_white
        else:
            self.bgcolour = grey_btn

    def set_pw(self, password):
        self.password = password

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        if self.password:
            strength = self.calc_strength()
            colour = self.setcolourandlabel(strength)
            update = self.FromDIP(wx.Size(strength, 10))
            dc.SetBrush(wx.Brush(self.bgcolour))
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
        if normalised_e > 100:
            normalised_e = 100
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

    def update(self, event):
        event.Skip()
        evt_source = event.EventObject
        password = evt_source.Value
        self.set_pw(password)
        self.Refresh()

class PWGenWindow(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetEscapeId(5101)
        self.pw_length = 24
        self.SetClientSize(self.FromDIP(wx.Size(500, 200)))
        self.generate_button = wx.Button(self, label="Generate Password")
        self.txt_ctrl = wx.TextCtrl(
            self,
            pos=(5, 5),
            size=(self.FromDIP(wx.Size(200, -1))),
            style=wx.TE_CENTRE,
        )
        self.spin_input = wx.SpinCtrl(
            self,
            style=wx.TE_PROCESS_ENTER,
            pos=(5, 15),
            min=8,
            max=32,
            initial=self.pw_length,
        )
        self.copy_button = wx.Button(self, label="Copy", size=(100, -1))
        self.autofill_button = wx.Button(self,id=wx.ID_OK, label="Use this password")
        self.choices_box = wx.CheckListBox(
            self,
            pos=(50, 50),
            choices=["Upper and Lowercase", "Digits", "Special Characters"],
        )
        self.choices_box.SetCheckedItems((0, 1, 2))

        self.strength_indicator = StrengthSizer(self, c_style=True)
        self.txt_ctrl.Bind(wx.EVT_TEXT, self.strength_indicator.strengthbar.update)
        self.indicator_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.indicator_sizer.Add(self.strength_indicator, 1, wx.ALIGN_CENTER_VERTICAL)

        self.generate_button.Bind(wx.EVT_BUTTON, self.generate_pw)
        self.copy_button.Bind(wx.EVT_BUTTON, self.copy_pw)
        self.spin_input.Bind(wx.EVT_SPINCTRL, self.set_pw_length)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer1.Add(self.generate_button, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.sub_sizer1.AddSpacer(10)
        self.sub_sizer1.Add(self.txt_ctrl, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.sub_sizer1.AddSpacer(10)
        self.sub_sizer1.Add(self.spin_input, 0, flag=wx.ALIGN_CENTRE_VERTICAL)

        self.sub_sizer2.Add(self.autofill_button, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sub_sizer2.AddSpacer(10)
        self.sub_sizer2.Add(self.copy_button, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.objects = [
            self.sub_sizer1,
            self.sub_sizer2,
            self.choices_box,
            self.indicator_sizer
        ]

        self.main_sizer.AddStretchSpacer()
        self.add_to_sizer(self.objects)
        self.main_sizer.AddStretchSpacer()
        self.SetSizer(self.main_sizer)

    def add_to_sizer(self, objects):
        for object in objects:
            self.main_sizer.Add(object, wx.SizerFlags().Centre().Border(wx.ALL, 15))

    def set_pw_length(self, event):
        self.pw_length = self.spin_input.GetValue()

    def set_pw_options(self, options):
        self.source_string = string.ascii_lowercase

        if 0 in options:
            self.source_string = string.ascii_letters
        if 1 in options:
            self.source_string += string.digits
        if 2 in options:
            self.source_string += string.punctuation
        return options
    def generate_pw(self, event):
        options = self.set_pw_options(self.choices_box.GetCheckedItems())
        while True:
            password = "".join(
                (secrets.choice(self.source_string) for i in range(self.pw_length))
            )
            if self.validate_pw(password, options) == True:
                break

        self.txt_ctrl.Clear()
        self.txt_ctrl.write(password)

    def validate_pw(self, password, options):
        if 0 in options:
            upperc = self.validate_upperc(password)
        else:
            upperc = True
        if 1 in options:
            nums = self.validate_nums(password)
        else:
            nums = True
        if 2 in options:
            symbols = self.validate_syms(password)
        else:
            symbols = True
        lowerc = self.validate_lowerc(password)
        if upperc and nums and symbols and lowerc == True:
            return True
        else:
            return False

    def validate_lowerc(self, password):
        if (any(char.islower() for char in password)):
            return True
        else:
            return False

    def validate_upperc(self, password):
        if (any(char.isupper() for char in password)):
            return True
        else:
            return False

    def validate_nums(self, password):
        if (sum(char.isdigit() for char in password) >= 3):
            return True
        else:
            return False

    def validate_syms(self, password):
        syms = re.sub("[\w]+", "", password)    # use regex to remove all 'word' characters
        count = len(syms)               # remaining chars will only be special characters
        if count >= 3:
            return True
        else:
            return False

    def check_strength(self, event):
        event.Skip()
        evt_source = event.EventObject
        password = evt_source.Value
        self.strength_indicator.strengthbar.set_pw(password)
        self.strength_indicator.strengthbar.Refresh()

    def copy_pw(self, event):
        self.txt_ctrl.SelectAll()
        self.txt_ctrl.Copy()

    def autofill(self, event):
        self.Destroy()



class DBpanel(wx.Panel):
    def __init__(self, parent, db=None):
        super().__init__(parent)
        self.db = db


class StaticText(wx.StaticText):
    def __init__(self, parent, label=None, c_style=None):
        super().__init__(parent)
        if label:
            self.SetLabel(label)
        if c_style:
            self.SetForegroundColour(black)
        else:
            self.SetForegroundColour(off_white)
