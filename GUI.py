import wx
import pprint
import ctypes

from modules import login_creator as login
from modules import db_manager as db_ops
import time

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
        list_box.SetScrollbar(20,20,50,50)
        self.rpanel = RightPanel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(list_box, 0, wx.EXPAND)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(self.rpanel, 0, wx.EXPAND)
        self.sizer.AddStretchSpacer()
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_list_box, list_box)

    def on_list_box(self, event):
        string = event.GetEventObject().GetStringSelection()
        self.rpanel.get_data(string)
        self.Parent.SendSizeEvent()


class RightPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.number_of_fields = 0
        self.frame = parent
        self.txtbox_sizer = wx.GridBagSizer(0, 0)

        while self.number_of_fields < 14:
            label = wx.StaticText(self)
            field = wx.TextCtrl(self)
            self.txtbox_sizer.Add(
                label, pos=(self.number_of_fields, 0), flag=wx.EXPAND | wx.ALL, border=10
            )
            self.txtbox_sizer.Add(
                field,
                pos=(self.number_of_fields, 1),
                flag=wx.EXPAND | wx.BOTTOM,
                border=10,
            )
            self.Bind(wx.EVT_TEXT, self.evt_text, field)
            self.Bind(wx.EVT_CHAR, self.evt_char, field)
            self.number_of_fields += 2

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_sizer.Add(self.txtbox_sizer, 3, wx.ALIGN_CENTRE)

        self.SetSizer(self.panel_sizer)
        self.Hide()

    def add_field(self):
        self.number_of_fields += 2
        new_label = wx.StaticText(self)
        new_field = wx.TextCtrl(self)
        self.Bind(wx.EVT_CHAR, self.evt_char, new_field)
        self.Bind(wx.EVT_TEXT, self.evt_text, new_field)
        self.txtbox_sizer.Add(
            new_label, pos=(self.number_of_fields, 0), flag=wx.EXPAND | wx.ALL, border=10
        )
        self.txtbox_sizer.Add(
            new_field,
            pos=(self.number_of_fields, 1),
            flag=wx.EXPAND | wx.BOTTOM,
            border=10,
        )

    def remove_field(self):
        if self.txtbox_sizer.GetChildren():
            sizer_item = self.txtbox_sizer.GetItem(self.number_of_fields - 1)
            sizer_item2 = self.txtbox_sizer.GetItem(self.number_of_fields - 2)
            field = sizer_item.GetWindow()
            field2 = sizer_item2.GetWindow()
            self.txtbox_sizer.Hide(field)
            self.txtbox_sizer.Hide(field2)
            field.Destroy()
            field2.Destroy()
            self.number_of_fields -= 2


    def get_data(self, string):
        self.Hide()
        self.data_obj = None
        uID = db.get_doc_id(string)
        doc = db.get_doc_by_id(uID)
        self.data_obj = db_ops.LoginData(doc)
        tic = time.perf_counter()
        self.on_view(self.data_obj.data)
        toc = time.perf_counter()
        self.Show()
        self.frame.SendSizeEvent()
        print(f"Function executed in {toc-tic:0.4f} seconds")

    def on_view(self, data_dict):
        dict_length = len(data_dict) * 2
        if dict_length == self.number_of_fields:
            self.add_data_to_view(data_dict)
        elif dict_length > self.number_of_fields:
            self.add_field()
            self.on_view(data_dict)
        elif dict_length < self.number_of_fields:
            self.remove_field()
            self.on_view(data_dict)

    def add_data_to_view(self, data_dict):
        i = 0
        key_index = 0
        value_index = 0
        dict_keys = list(data_dict.keys())
        dict_values = list(data_dict.values())
        for sizer_item in self.txtbox_sizer.__iter__():
            item = sizer_item.GetWindow()
            if i % 2 == 0:
                item.SetLabel(dict_keys[key_index])
                key_index += 1
            else:
                text = dict_values[value_index]
                item.SetLabel(text)
                size = item.GetSizeFromText(text)
                item.SetMinSize(size)
                value_index += 1
            i += 1


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
