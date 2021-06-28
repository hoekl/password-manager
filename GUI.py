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

        self.text_control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(list_box, 0, wx.EXPAND)
        sizer.Add(self.text_control, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_list_box, list_box)

    def on_list_box(self, event):
        self.text_control.Clear()
        string = event.GetEventObject().GetStringSelection()
        self.text_control.AppendText("Current select: " + string + "\n\n")
        uID = db.get_doc_id(string)
        doc = db.get_doc_by_id(uID)
        data_dict = db_ops.LoginData(doc)
        key_list, value_list = data_dict.format_data()

        for key, value in zip(key_list, value_list):
            self.text_control.AppendText(key + ": " + value + "\n")


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
