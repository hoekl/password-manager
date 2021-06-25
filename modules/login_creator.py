import secrets
import string
import wx


class MainPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        pwGenButton = wx.Button(self, label="Generate Password")
        pwGenButton.Bind(wx.EVT_BUTTON, self.onGenerate)
        main_sizer.Add(pwGenButton, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        self.SetSizer(main_sizer)

    def onGenerate(self, event):
        dialog = PWGenWindow()
        dialog.ShowModal()
        dialog.Destroy()


class PWGenWindow(wx.Dialog):
    def __init__(self):
        super().__init__(parent=None, title="Generate new password")
        self.pwLength = 12
        self.SetClientSize(self.FromDIP(wx.Size(500, 200)))
        self.pwGenButton = wx.Button(self, label="Generate Password")
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
            initial=self.pwLength,
        )
        self.checkListBox = wx.CheckListBox(
            self,
            pos=(50, 50),
            choices=["Upper and Lowercase", "Digits", "Special Characters"],
        )
        self.checkListBox.SetCheckedItems((0, 1, 2))
        self.pwGenButton.Bind(wx.EVT_BUTTON, self.generatePW)
        self.spin_input.Bind(wx.EVT_SPINCTRL, self.setPWLength)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.objects = [
            self.txt_ctrl,
            self.pwGenButton,
            self.spin_input,
            self.checkListBox,
        ]
        #self.middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.AddStretchSpacer()
        self.addToSizer(self.objects)
        self.main_sizer.AddStretchSpacer()
        #self.middle_sizer.Add(self.main_sizer, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        self.SetSizer(self.main_sizer)

    def addToSizer(self, objects):
        for object in objects:
            self.main_sizer.Add(object, wx.SizerFlags().Centre().Border(wx.ALL, 5))

    def setPWLength(self, event):
        self.pwLength = self.spin_input.GetValue()

    def getPWOptions(self, options):
        self.sourceString = string.ascii_lowercase

        if 0 in options:
            self.sourceString = string.ascii_letters
        if 1 in options:
            self.sourceString += string.digits
        if 2 in options:
            self.sourceString += string.punctuation

    def generatePW(self, event):
        self.getPWOptions(self.checkListBox.GetCheckedItems())
        password = "".join(
            (secrets.choice(self.sourceString) for i in range(self.pwLength))
        )
        self.txt_ctrl.Clear()
        self.txt_ctrl.write(password)
