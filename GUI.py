import wx
import pprint
import ctypes
import wx.lib.agw.flatnotebook as flnb

from modules import login_creator as login
from modules import db_manager as db_ops
from modules import view_panel as vp
from modules import custom_widgets as cw
from modules import encryption_handler as crypto
from lockout_manager import Lockout

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass
pp = pprint.PrettyPrinter(indent=4)


dark_grey = wx.Colour(38, 38, 38)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(55, 55, 55)


class LoginScreen(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.db = db_ops.DataBase("encrypted_mock_data")
        self.authenticated = False
        self.verify_db = db_ops.verify_db
        if self.db.is_new == True:
            if self.existing_db_check() == False:
                password = self.create_password()
                key_manager = crypto.CryptoKeyManager(password, True)
                self.verify_db.setup(key_manager)
            else:
                key_manager = self.import_existing()
                self.verify_db.setup(key_manager)
        self.lockout = Lockout()
        while self.authenticated == False:
            if self.lockout.check_access() == True:
                self.get_pw()
            else:
                self.locked_message()

        fernet_obj = db_ops.Fernet_obj(self.fernet)
        self.db.set_fernet(fernet_obj)
        frm = BaseFrame(None, title="   Password Manager", db=self.db)
        frm.SetClientSize(frm.FromDIP(wx.Size(1000, 500)))
        frm.SetIcon(wx.Icon("modules/Icons/padlock_78356.ico", wx.BITMAP_TYPE_ICO))
        frm.Show()
        self.Destroy()

    def existing_db_check(self):
        dialog = wx.MessageDialog(
            self,
            "Would you like to import an existing database?",
            "Import existing?",
            style=wx.YES_NO | wx.CANCEL,
        )
        res = dialog.ShowModal()
        if res == wx.ID_YES:
            return True
        elif res == wx.ID_NO:
            return False
        elif res == wx.ID_CANCEL:
            wx.Exit()

    def import_existing(self):
        with wx.FileDialog(
            self, "Choose database file to import", wildcard="*.tar"
        ) as fileDialog:
            fileDialog.SetMessage("Choose database file to import")
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            tar_path = fileDialog.GetPath()
        with wx.MessageDialog(
            self,
            "Please specify location of salt to import",
            "Salt location",
            style=wx.OK | wx.CENTRE,
        ) as msgDialog:
            if msgDialog.ShowModal() == wx.ID_CANCEL:
                return
        with wx.FileDialog(
            self, "Choose salt location", wildcard="*.key"
        ) as fileDialog:
            fileDialog.SetMessage("Choose salt location")
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            salt_path = fileDialog.GetPath()

        dialog = wx.PasswordEntryDialog(
            self,
            message="Enter password for this database",
            style=wx.OK | wx.CANCEL | wx.CENTRE,
        )
        res = dialog.ShowModal()
        if res == 5100:
            password = dialog.Value
        dialog.Destroy()
        key_manager = crypto.CryptoKeyManager(password)
        key_manager.import_salt(salt_path, password)
        try:
            self.db.import_db(tar_path)
            with wx.MessageDialog(
                self,
                message="Database exported successfully",
                caption="Success",
                style=wx.OK,
            ) as dialog:
                dialog.ShowModal()
            return key_manager
        except Exception as e:
            print(e)
            with wx.MessageDialog(
                self,
                message="Something went wrong, please try again",
                caption="Error",
                style=wx.OK,
            ) as dialog:
                dialog.ShowModal()

    def get_pw(self):
        dialog = wx.PasswordEntryDialog(
            self, message="Enter your password", style=wx.OK | wx.CANCEL | wx.CENTRE
        )
        res = dialog.ShowModal()
        if res == 5100:
            password = dialog.Value
            self.fernet = self.verify_db.verify_password(password)
            dialog.Destroy()
            if self.fernet:
                self.authenticated = True
                self.lockout.clear_lockout()
                return True
            else:
                self.lockout.increase_count()
                if self.lockout.tries >= 5:
                    self.lockout.trigger_lockout()
                return False
        if res == 5101:
            wx.Exit()

    def create_password(self):
        dialog = wx.PasswordEntryDialog(
            self,
            message="Enter new master password",
            style=wx.OK | wx.CANCEL | wx.CENTRE,
        )
        res = dialog.ShowModal()
        if res == 5100:
            password = dialog.Value
            dialog.Destroy()
            return password
        if res == 5101:
            wx.Exit()

    def locked_message(self):
        with wx.MessageDialog(
            self,
            message="Incorrect password entered too many times",
            caption="Locked account",
            style=wx.OK,
        ) as lockoutDialog:
            if lockoutDialog.ShowModal() == wx.ID_OK:
                wx.Exit()


class BaseFrame(wx.Frame):
    def __init__(self, parent, title=None, db=None):
        super(BaseFrame, self).__init__(parent, title=title)
        self.db = db
        self.CreateStatusBar()
        self.create_menu_bar()
        font = self.GetFont()
        font.SetPointSize(11)
        self.SetFont(font)
        self.StatusBar.SetBackgroundColour(light_grey)
        self.SetBackgroundColour(dark_grey)
        self.base_panel = cw.DBpanel(self, self.db)
        self.notebook = flnb.FlatNotebook(
            self.base_panel,
            agwStyle=flnb.FNB_NO_NAV_BUTTONS
            | flnb.FNB_NO_X_BUTTON
            | flnb.FNB_NODRAG
            | flnb.FNB_DEFAULT_STYLE,
        )
        self.notebook.SetBackgroundColour(dark_grey)
        self.login_panel = login.CreateLogin(self.notebook)
        self.view_panel = ListPanel(self.notebook)
        self.notebook.AddPage(self.login_panel, "New Login", False)
        self.notebook.AddPage(self.view_panel, "Logins", True)

        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.notebook_sizer.Add(self.notebook, 1, flag=wx.EXPAND)
        self.base_panel.SetSizer(self.notebook_sizer)

    def refresh(self, show):
        self.notebook.DeletePage(1)
        new_list_panel = ListPanel(self.notebook)
        self.notebook.AddPage(new_list_panel, "Logins", show)

    def create_menu_bar(self):
        db_menu = wx.Menu()
        edit_menu = wx.Menu()
        db_dump = db_menu.Append(-1, "&Export Database \tCtrl-E")
        change_pw = edit_menu.Append(-1, "&Change Master Password \tCtrl+P")
        menu_bar = wx.MenuBar()
        menu_bar.Append(db_menu, "&Database")
        menu_bar.Append(edit_menu, "&Edit")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.dump_db, db_dump)
        self.Bind(wx.EVT_MENU, self.change_password, change_pw)

    def dump_db(self, event):
        with wx.DirDialog(self, "Choose save location") as fileDialog:
            fileDialog.SetMessage("Choose save location")
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path_name = fileDialog.GetPath()
        try:
            self.db.dump(path_name)
            with wx.MessageDialog(
                self,
                message="Database exported successfully",
                caption="Success",
                style=wx.OK,
            ) as dialog:
                dialog.ShowModal()
        except Exception as e:
            print(e)
            with wx.MessageDialog(
                self,
                message="Something went wrong, please try again",
                caption="Error",
                style=wx.OK,
            ) as dialog:
                dialog.ShowModal()

    def change_password(self, *event):
        existing_pw = self.get_existingpw()
        new_pw = self.new_pw_entry()
        existing_keymngr = crypto.CryptoKeyManager(existing_pw)
        new_keymngr = crypto.CryptoKeyManager(new_pw, True)
        try:
            self.db.change_masterpw(new_keymngr.fernet, existing_keymngr.fernet)
            dialog = wx.MessageDialog(
                self, "Password change successful", "Success!", style=wx.OK | wx.CENTRE
            )
            dialog.ShowModal()
            dialog.Destroy()
            new_fernet = db_ops.Fernet_obj(new_keymngr.fernet)
            self.base_panel.db.set_fernet(new_fernet)
            self.Freeze()
            self.refresh(True)
            self.Thaw()
        except Exception as e:
            print(e)

    def get_existingpw(self):
        with wx.PasswordEntryDialog(
            self,
            "Enter your existing password",
            "Existing password",
            style=wx.OK | wx.CANCEL | wx.CENTRE,
        ) as pwDialog:
            if pwDialog.ShowModal() == wx.ID_CANCEL:
                return
            existing_pw = pwDialog.Value
            check = db_ops.verify_db.verify_password(existing_pw)
            if check:
                return existing_pw
            else:
                with wx.MessageDialog(
                    self,
                    "Incorrect Password, please try again",
                    "Incorrect Password",
                    style=wx.OK | wx.CENTRE,
                ) as alertDialog:
                    if alertDialog.ShowModal() == wx.ID_OK:
                        self.change_password()
                    else:
                        return

    def new_pw_entry(self):
        new_pw = self.get_new_pw("Enter your new password", "New password")
        check_newpw = self.get_new_pw("Confirm your new password", "Confirm password")
        if new_pw != check_newpw:
            infoDialog = wx.MessageDialog(
                self,
                "New passwords do not match, please try again",
                "No match",
                style=wx.OK | wx.CENTRE,
            )
            infoDialog.ShowModal()
            infoDialog.Destroy()
            return self.new_pw_entry()
        else:
            return check_newpw

    def get_new_pw(self, message, caption):
        with wx.PasswordEntryDialog(
            self, message, caption, style=wx.OK | wx.CANCEL | wx.CENTRE
        ) as newPwDialog:
            if newPwDialog.ShowModal() == wx.ID_CANCEL:
                return
            return newPwDialog.Value


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(dark_grey)
        choices = self.GrandParent.db.get_logins_list()
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
        uID = self.GrandParent.db.get_doc_id(string)
        doc = self.GrandParent.db.get_doc_by_id(uID)
        self.view_panel.show_data(doc)
        self.SendSizeEvent()
        self.view_panel.Thaw()


if __name__ == "__main__":
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    app.SetExitOnFrameDelete(True)
    screen = LoginScreen(None)
    app.MainLoop()
