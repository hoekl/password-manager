import wx
from wx.core import ListCtrl

from modules import login_creator as login

class BaseFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)

        noteBookPanel = wx.Notebook(self)
        firstPanel = login.MainPanel(noteBookPanel)     #implement own class to add functionality
        secondPanel = ListPanel(noteBookPanel)
        noteBookPanel.AddPage(firstPanel, "New Login", True)
        noteBookPanel.AddPage(secondPanel, "Logins", True)

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(firstPanel, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        frameSizer.Add(secondPanel, wx.SizerFlags().Centre().Border(wx.ALL, 5))

class ListPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)

        #listctrl = wx.ListCtrl(self, size=(900, 400), style=wx.LC_REPORT, name=("All Logins"))
        testItems = ["amazon.com", "twitter.com", "oracle.com"]
        listBox = wx.ListBox(self, size=(400, -1), choices = testItems, style=wx.LB_SINGLE)
        self.textControl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer.Add(listctrl, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        sizer.Add(listBox, 0, wx.EXPAND)
        sizer.Add(self.textControl, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_LISTBOX, self.onListBox, listBox)

    def onListBox(self, event):
        self.textControl.AppendText("Current select:" + event.GetEventObject().GetStringSelection()+"\n")

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = BaseFrame(None, title='Password Manager', size=(1000,500))
    frm.Show()
    app.MainLoop()

