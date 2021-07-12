import wx
import pprint
import ctypes
import wx.lib.agw.flatnotebook as flnb


from modules import login_creator as login
from modules import db_manager as db_ops
from modules import view_panel as vp

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
pp = pprint.PrettyPrinter(indent=4)

dark_grey = wx.Colour(42, 42, 46)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(53, 53, 59)
class BaseFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour(light_grey)
        self.SetBackgroundColour(dark_grey)
        self.SetForegroundColour(off_white)
        self.base_panel = wx.Panel(self)

        self.notebook = flnb.FlatNotebook(self.base_panel, agwStyle=flnb.FNB_NO_NAV_BUTTONS | flnb.FNB_NO_X_BUTTON | flnb.FNB_NODRAG | flnb.FNB_DEFAULT_STYLE)
        self.notebook.SetBackgroundColour(dark_grey)
        first_panel = login.CreateLogin(self.notebook)
        first_panel.SetBackgroundColour(dark_grey)
        second_panel = ListPanel(self.notebook)
        second_panel.SetBackgroundColour(dark_grey)
        self.notebook.AddPage(first_panel, "New Login", False)
        self.notebook.AddPage(second_panel, "Logins", True)

        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.notebook_sizer.Add(self.notebook, 1, flag=wx.EXPAND)
        self.base_panel.SetSizer(self.notebook_sizer)

    def refresh(self):
        self.notebook.DeletePage(1)
        new_list_panel = ListPanel(self.notebook)
        self.notebook.AddPage(new_list_panel, "Logins", False)


class ListPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)
        self.SetBackgroundColour(dark_grey)
        choices = db_ops.db.get_logins_list()
        self.list_box = wx.ListBox(
            self, size=(400, -1), choices=choices, style=wx.LB_SINGLE | wx.LB_SORT | wx.BORDER_NONE
        )
        self.list_box.SetBackgroundColour(dark_grey)
        self.list_box.SetForegroundColour(off_white)
        self.list_box.SetScrollbar(20, 20, 50, 50)
        self.list_box.SetBackgroundColour(dark_grey)
        self.view_panel = vp.ViewPanel(self)
        self.view_panel.SetForegroundColour(off_white)
        self.view_panel.SetBackgroundColour(dark_grey)
        self.view_panel.Hide()
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.list_box, 0, wx.EXPAND)
        self.sizer.Add(self.view_panel, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_select_item, self.list_box)


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
    frm = BaseFrame(None, title="   Password Manager")
    frm.SetClientSize(frm.FromDIP(wx.Size(1000, 500)))
    frm.SetIcon(wx.Icon("modules/Icons/padlock_78356.ico", wx.BITMAP_TYPE_ICO))
    frm.Show()
    app.MainLoop()
