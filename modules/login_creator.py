import secrets
import string
import wx


class MainPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        launch_dialog = wx.Button(self, label="Generate Password")
        launch_dialog.Bind(wx.EVT_BUTTON, self.on_generate)
        main_sizer.Add(launch_dialog, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        self.SetSizer(main_sizer)

    def on_generate(self, event):
        dialog = PWGenWindow()
        dialog.ShowModal()
        dialog.Destroy()


class PWGenWindow(wx.Dialog):
    def __init__(self):
        super().__init__(parent=None, title="Generate new password")
        self.pw_length = 12
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
            max=24,
            initial=self.pw_length,
        )
        self.choices_box = wx.CheckListBox(
            self,
            pos=(50, 50),
            choices=["Upper and Lowercase", "Digits", "Special Characters"],
        )
        self.choices_box.SetCheckedItems((0, 1, 2))
        self.generate_button.Bind(wx.EVT_BUTTON, self.generate_pw)
        self.spin_input.Bind(wx.EVT_SPINCTRL, self.set_pw_length)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.objects = [
            self.txt_ctrl,
            self.generate_button,
            self.spin_input,
            self.choices_box,
        ]

        self.main_sizer.AddStretchSpacer()
        self.add_to_sizer(self.objects)
        self.main_sizer.AddStretchSpacer()
        self.SetSizer(self.main_sizer)

    def add_to_sizer(self, objects):
        for object in objects:
            self.main_sizer.Add(object, wx.SizerFlags().Centre().Border(wx.ALL, 5))

    def set_pw_length(self):
        self.pw_length = self.spin_input.GetValue()

    def set_pw_options(self, options):
        self.source_string = string.ascii_lowercase

        if 0 in options:
            self.source_string = string.ascii_letters
        if 1 in options:
            self.source_string += string.digits
        if 2 in options:
            self.source_string += string.punctuation

    def generate_pw(self, event):
        self.set_pw_options(self.choices_box.GetCheckedItems())
        password = "".join(
            (secrets.choice(self.source_string) for i in range(self.pw_length))
        )
        self.txt_ctrl.Clear()
        self.txt_ctrl.write(password)


if __name__ == "__main__":
    pass
