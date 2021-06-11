import secrets
import string
import wx

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        pwGenButton = wx.Button(self, label='Generate Password')
        pwGenButton.Bind(wx.EVT_BUTTON, self.onGenerate)
        main_sizer.Add(pwGenButton, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        self.SetSizer(main_sizer)

    def onGenerate(self, event):
        dialog = PWGenWindow()
        dialog.ShowModal()
        dialog.Destroy()

class PWGenWindow(wx.Dialog):
    def __init__(self):
        super().__init__(parent=None, title='Generate new password')
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        pwGenButton = wx.Button(self, label='Generate Password')
        self.main_sizer.Add(pwGenButton, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        self.SetSizer(self.main_sizer)
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Password Manager')
        self.panel = MainPanel(self)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

def pw_gen(pw_length):
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(pw_length)))
    return(password)

#print(pw_gen(10))

