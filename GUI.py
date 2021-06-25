import wx
import pprint
from modules import login_creator as login
from modules import db_manager as db

pp = pprint.PrettyPrinter(indent=4)


class BaseFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)

        noteBookPanel = wx.Notebook(self)
        firstPanel = login.MainPanel(
            noteBookPanel
        )  # implement own class to add functionality
        secondPanel = ListPanel(noteBookPanel)
        noteBookPanel.AddPage(firstPanel, "New Login", True)
        noteBookPanel.AddPage(secondPanel, "Logins", True)

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(firstPanel, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        frameSizer.Add(secondPanel, wx.SizerFlags().Centre().Border(wx.ALL, 5))


class ListPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)

        choicesList = self.getLoginsFromDB()
        listBox = wx.ListBox(
            self, size=(400, -1), choices=choicesList, style=wx.LB_SINGLE | wx.LB_SORT
        )

        self.textControl = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(listBox, 0, wx.EXPAND)
        sizer.Add(self.textControl, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, self.onListBox, listBox)



    def onListBox(self, event):
        self.textControl.Clear()
        string = event.GetEventObject().GetStringSelection()
        self.textControl.AppendText(
            "Current select: " + string + "\n\n"
        )
        doc = db.getDocByID(self.linkDict, string)
        listKeys = list(doc.keys())
        listValues = list(doc.values())
        listKeys.pop(0)
        listKeys.pop(0)
        listValues.pop(0)
        listValues.pop(0)

        for i in range(len(listKeys)):
            strKey = str(listKeys[i])
            strVal = str(listValues[i])
            self.textControl.AppendText(strKey + ": " + strVal + "\n")



    def getLoginsFromDB(self):
        res = db.QueryAll()
        self.linkDict = db.formatQueryRes(res)
        choicesList = list(self.linkDict.keys())

        return choicesList
        # pp.pprint(res)


if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    db = db.DataBase("mock_data")
    frm = BaseFrame(None, title="Password Manager", size=(1000, 500))
    frm.Show()
    app.MainLoop()
