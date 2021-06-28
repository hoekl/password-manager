from typing import List
import wx
import pprint
import ctypes
from modules import login_creator as login
from modules import db_manager as db_ops

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
pp = pprint.PrettyPrinter(indent=4)


class BaseFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)
        self.CreateStatusBar()
        notebook_panel = wx.Notebook(self)
        first_panel = login.MainPanel(notebook_panel)
        second_panel = ListPanel(notebook_panel)
        notebook_panel.AddPage(first_panel, "New Login", True)
        notebook_panel.AddPage(second_panel, "Logins", True)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(first_panel, wx.SizerFlags().Centre().Border(wx.ALL, 5))
        frame_sizer.Add(second_panel, wx.SizerFlags().Centre().Border(wx.ALL, 5))


class ListPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)

        choices = db.get_logins_list()
        list_box = wx.ListBox(
            self, size=(400, -1), choices=choices, style=wx.LB_SINGLE | wx.LB_SORT
        )

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(list_box, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_list_box, list_box)

    def on_list_box(self, event):
        display_panel = LoginsPanel(self)
        string = event.GetEventObject().GetStringSelection()
        display_panel.create_and_show(string)

        if self.sizer.GetItemCount() > 1:
            sizer_item = self.sizer.GetItem(1)
            panel = sizer_item.GetWindow()
            self.sizer.Hide(panel)
            panel.Destroy()

            self.sizer.Add(display_panel, 1, wx.EXPAND)
        else:
            self.sizer.Add(display_panel, 1, wx.EXPAND)

        self.sizer.Layout()


class LoginsPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(LoginsPanel, self).__init__(*args, **kw)


    def create_and_show(self, string):
        self.txtbox_sizer = wx.BoxSizer(wx.VERTICAL)
        self.entries = []

        uID = db.get_doc_id(string)
        doc = db.get_doc_by_id(uID)
        data_dict = db_ops.LoginData(doc)
        index = 0
        for key, value in data_dict.data.items():
            self.label = wx.StaticText(self, label=key)
            self.entries.append(wx.TextCtrl(self, value=value))
            self.txtbox_sizer.Add(self.label, 1, wx.EXPAND | wx.ALL, 0)
            self.txtbox_sizer.Add(self.entries[index], 3, wx.EXPAND | wx.BOTTOM, 10)
            self.Bind(wx.EVT_TEXT, self.evt_text, self.entries[index])
            self.Bind(wx.EVT_CHAR, self.evt_char, self.entries[index])
            index += 1

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_sizer.Add(self.txtbox_sizer, 2, wx.EXPAND)

        self.SetSizer(self.panel_sizer)
        self.panel_sizer.Fit(self)
        self.Show()


    def evt_text(self, event):
        pass

    def evt_char(self, event):
        pass


if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    db = db_ops.DataBase("mock_data")
    frm = BaseFrame(None, title="   Password Manager")
    frm.SetClientSize(frm.FromDIP(wx.Size(1000, 500)))
    frm.SetIcon(wx.Icon("modules/Icons/padlock_78356.ico", wx.BITMAP_TYPE_ICO))
    frm.Show()
    app.MainLoop()
