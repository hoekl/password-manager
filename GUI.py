import wx
import pprint
import ctypes


from modules import login_creator as login
from modules import db_manager as db_ops
from modules import view_panel as vp

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
pp = pprint.PrettyPrinter(indent=4)


class BaseFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)
        self.CreateStatusBar()
        notebook_panel = wx.Notebook(self, style=wx.BORDER_SIMPLE)
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

        choices = db_ops.db.get_logins_list()
        self.list_box = wx.ListBox(
            self, size=(400, -1), choices=choices, style=wx.LB_SINGLE | wx.LB_SORT
        )
        self.list_box.SetScrollbar(20, 20, 50, 50)
        self.view_panel = vp.ViewPanel(self)
        self.view_panel.Hide()
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.list_box, 0, wx.EXPAND)
        self.sizer.Add(self.view_panel, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_select_item, self.list_box)

    def get_logins_list(self):
        choices = db_ops.db.get_logins_list()
        list_box = wx.ListBox(
            self, size=(400, -1), choices=choices, style=wx.LB_SINGLE | wx.LB_SORT
        )
        return list_box


    def on_select_item(self, event):
        index = self.list_box.GetSelection()
        string = self.list_box.GetString(index)
        self.view_panel.Show()
        self.view_panel.Freeze()
        uID = db_ops.db.get_doc_id(string)
        doc = db_ops.db.get_doc_by_id(uID)
        self.view_panel.show_data(doc)
        self.SendSizeEvent()
        self.view_panel.Thaw()




if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    #db = db_ops.DataBase("copy_mock_data")
    frm = BaseFrame(None, title="   Password Manager")
    frm.SetClientSize(frm.FromDIP(wx.Size(900, 500)))
    frm.SetIcon(wx.Icon("modules/Icons/padlock_78356.ico", wx.BITMAP_TYPE_ICO))
    frm.Show()
    app.MainLoop()
