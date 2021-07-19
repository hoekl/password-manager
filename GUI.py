import wx
import pprint
import ctypes
import wx.lib.agw.flatnotebook as flnb


from modules import login_creator as login
from modules import db_manager as db_ops
from modules import view_panel as vp
from modules import custom_widgets as cw

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
pp = pprint.PrettyPrinter(indent=4)


dark_grey = wx.Colour(38, 38, 38)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(55, 55, 55)


class BaseFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)
        self.authenticated = False
        while self.authenticated == False:
            if self.get_pw() == False:
                self.get_pw()
            else:
                self.authenticated = True
        self.CreateStatusBar()
        font = self.GetFont()
        font.SetPointSize(11)
        self.SetFont(font)
        self.StatusBar.SetBackgroundColour(light_grey)
        self.SetBackgroundColour(dark_grey)
        self.SetForegroundColour(off_white)
        self.base_panel = wx.Panel(self)

        self.notebook = flnb.FlatNotebook(
            self.base_panel,
            agwStyle=flnb.FNB_NO_NAV_BUTTONS
            | flnb.FNB_NO_X_BUTTON
            | flnb.FNB_NODRAG
            | flnb.FNB_DEFAULT_STYLE,
        )
        self.notebook.SetBackgroundColour(dark_grey)
        first_panel = login.CreateLogin(self.notebook, self.fernet)
        second_panel = ListPanel(self.notebook, self.fernet)
        self.notebook.AddPage(first_panel, "New Login", False)
        self.notebook.AddPage(second_panel, "Logins", True)

        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.notebook_sizer.Add(self.notebook, 1, flag=wx.EXPAND)
        self.base_panel.SetSizer(self.notebook_sizer)

    def refresh(self):
        self.notebook.DeletePage(1)
        new_list_panel = ListPanel(self.notebook, self.fernet)
        self.notebook.AddPage(new_list_panel, "Logins", False)

    def get_pw(self):
        dialog = wx.PasswordEntryDialog(
            self, message="Enter your password", style=wx.OK | wx.CANCEL
        )
        res = dialog.ShowModal()
        if res == 5100:
            password = dialog.Value
            salt = db_ops.verify_password(password)
            self.fernet = db_ops.Fernet_obj(salt, password)
            dialog.Destroy()
            if salt:
                return True
            else:
                return False
        if res == 5101:
            wx.Exit()


class ListPanel(wx.Panel):
    def __init__(self, parent, fernet=None):
        super().__init__(parent)
        if fernet:
            self.fernet = fernet
        self.SetBackgroundColour(dark_grey)
        choices = db_ops.db.get_logins_list(self.fernet)
        self.choices = sorted(choices)
        self.list_box = wx.ListBox(
            self,
            size=(400, -1),
            choices=self.choices,
            style=wx.LB_SINGLE | wx.BORDER_NONE,
        )

        self.searchbox = cw.TextCtrl(
            self, value="\U0001F50E Search...", style=wx.BORDER_SIMPLE
        )
        self.searchbox.Bind(wx.EVT_KEY_UP, self.search)
        self.searchbox.Bind(wx.EVT_SET_FOCUS, self.clear_search)
        self.searchbox.Bind(wx.EVT_KILL_FOCUS, self.set_search)
        self.list_box.SetForegroundColour(off_white)
        self.list_box.SetBackgroundColour(dark_grey)
        self.view_panel = vp.ViewPanel(self)
        self.view_panel.SetForegroundColour(off_white)
        self.view_panel.SetBackgroundColour(dark_grey)
        self.view_panel.Hide()
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer.Add(self.searchbox, 0, wx.EXPAND)
        self.sub_sizer.Add(self.list_box, 1, wx.EXPAND)
        self.sizer.Add(self.sub_sizer, 0, wx.EXPAND)
        self.sizer.Add(self.view_panel, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_select_item, self.list_box)

    def search(self, event):
        event.Skip()
        self.list_box.Freeze()
        get_char = self.searchbox.GetValue()
        self.list_box.Clear()
        for item in self.choices:
            if get_char in item:
                self.list_box.Append(item)
        self.list_box.Thaw()

    def clear_search(self, event):
        event.Skip()
        selected_index = self.list_box.GetSelection()
        try:
            self.selected_string = self.list_box.GetString(selected_index)
        except Exception:
            pass
        self.searchbox.Clear()
        send_backspace = wx.UIActionSimulator()
        send_backspace.Char(8)

    def set_search(self, event):
        event.Skip()
        try:
            self.list_box.SetStringSelection(self.selected_string)
        except Exception:
            pass
        self.searchbox.SetValue("\U0001F50E Search...")

    def on_select_item(self, *event):
        index = self.list_box.GetSelection()
        string = self.list_box.GetString(index)
        self.view_panel.Show()
        self.view_panel.Freeze()
        if self.view_panel.is_edited == True:
            self.view_panel.to_readonly()
        uID = db_ops.db.get_doc_id(string)
        doc = db_ops.db.get_doc_by_id(uID)
        decrypted_doc = self.fernet.decrypt_individual(doc)
        self.view_panel.show_data(decrypted_doc)
        self.SendSizeEvent()
        self.view_panel.Thaw()


if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    app.SetExitOnFrameDelete(True)
    frm = BaseFrame(None, title="   Password Manager")
    frm.SetClientSize(frm.FromDIP(wx.Size(1000, 500)))
    frm.SetIcon(wx.Icon("modules/Icons/padlock_78356.ico", wx.BITMAP_TYPE_ICO))
    frm.Show()
    app.MainLoop()
