import wx
import time
from modules import db_manager as db_ops

db = db_ops.DataBase("mock_data")


class ViewPanel(wx.Panel):
    def __init__(self, *agrs, **kw):
        super().__init__(*agrs, **kw)
        self.number_of_fields = 0
        self.txtbox_sizer = wx.GridBagSizer(0, 0)
        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bounding_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)


        while self.number_of_fields < 14:
            label = wx.StaticText(self)
            field = wx.TextCtrl(self)
            self.txtbox_sizer.Add(
                label,
                pos=(self.number_of_fields, 0),
                flag=wx.EXPAND | wx.ALL,
                border=10,
            )
            self.txtbox_sizer.Add(
                field,
                pos=(self.number_of_fields, 1),
                flag=wx.EXPAND | wx.ALL,
                border=10,
            )
            self.number_of_fields += 2

        self.btn_edit = wx.Button(self, label="Edit", size=(100, 50))
        self.btn_save = wx.Button(self, label="Save", size=(100, 50))
        self.btn_show_pw = wx.Button(self, label="Show Password", size=(250,50))
        self.btn_hide_pw = wx.Button(self, label="Hide Password", size=(250,50))
        self.btn_copy_pw = wx.Button(self, label="Copy Password", size=(250,50))
        self.btn_edit.Bind(wx.EVT_BUTTON, self.set_editable)
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_edits)
        self.btn_copy_pw.Bind(wx.EVT_BUTTON, self.copy_pw)
        self.btn_show_pw.Bind(wx.EVT_BUTTON, self.show_pw)
        self.btn_hide_pw.Bind(wx.EVT_BUTTON, self.hide_pw)


        self.panel_sizer.AddStretchSpacer()
        self.bounding_sizer.Add(self.txtbox_sizer, 3, wx.ALIGN_CENTER)
        self.button_sizer.Add(self.btn_edit, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(self.btn_save, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(25,50)
        self.button_sizer.Add(self.btn_show_pw, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(self.btn_hide_pw, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(25,50)
        self.button_sizer.Add(self.btn_copy_pw, 0, wx.ALIGN_CENTER, border=50)
        self.bounding_sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTRE)
        self.panel_sizer.Add(self.bounding_sizer, 3, wx.ALIGN_CENTER)
        self.panel_sizer.AddStretchSpacer()
        self.SetSizer(self.panel_sizer)
        self.btn_save.Hide()
        self.btn_show_pw.Hide()


    def add_field(self):
        self.number_of_fields += 2
        new_label = wx.StaticText(self)
        new_field = wx.TextCtrl(self)
        self.txtbox_sizer.Add(
            new_label,
            pos=(self.number_of_fields, 0),
            flag=wx.EXPAND | wx.ALL,
            border=10,
        )
        self.txtbox_sizer.Add(
            new_field,
            pos=(self.number_of_fields, 1),
            flag=wx.EXPAND | wx.ALL,
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

    def show_data(self, doc):
        self.btn_hide_pw.Hide()
        self.btn_show_pw.Show()
        tic = time.perf_counter()

        self.current_dataobj = db_ops.LoginData(doc)

        self.create_view(self.current_dataobj.data)

        toc = time.perf_counter()

        print(f"Function executed in {toc-tic:0.4f} seconds")

    def create_view(self, data_dict):
        dict_length = len(data_dict) * 2
        if dict_length == self.number_of_fields:
            self.remove_pw_field()
            self.add_data_to_view(data_dict)
        elif dict_length > self.number_of_fields:
            self.add_field()
            self.create_view(data_dict)
        elif dict_length < self.number_of_fields:
            self.remove_field()
            self.create_view(data_dict)

    def remove_pw_field(self):
        for sizer_item in self.txtbox_sizer.__iter__():
            ctrl = sizer_item.GetWindow()
            if ctrl.GetName() == "password":
                self.txtbox_sizer.Hide(ctrl)
                temp_ctrl = wx.TextCtrl(self)
                self.txtbox_sizer.Replace(ctrl, temp_ctrl)
                ctrl.Destroy()


    def add_data_to_view(self, data_dict):
        parent_size = self.Parent.sizer.GetSize()
        size_x = parent_size[0]*0.6
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
                item.SetName(dict_keys[value_index])
                size_y = item.GetBestHeight(size_x)
                new_size = (size_x, size_y)
                item.SetMinSize(new_size)
                item.SetEditable(False)
                value_index += 1
            i += 1

        self.set_style_pw()

    def set_style_pw(self):

        i = 0
        for item in self.txtbox_sizer.__iter__():
            if i % 2 == 0:
                pass
            else:
                ctrl = item.GetWindow()
                if ctrl.GetName() == "password":
                    pw_ctrl = wx.TextCtrl(self, value="abcdefg", style= wx.TE_READONLY | wx.TE_PASSWORD)
                    pw_ctrl.SetName("password")
                    self.txtbox_sizer.Hide(ctrl)
                    self.txtbox_sizer.Replace(ctrl, pw_ctrl)
                    ctrl.Destroy()
                    break
            i += 1


    def set_editable(self, event):
        i = 0
        self.show_pw(event)
        self.btn_show_pw.Hide()
        self.btn_hide_pw.Hide()
        for sizer_item in self.txtbox_sizer.__iter__():
            item = sizer_item.GetWindow()
            if i % 2 == 0:
                pass
            else:
                item.SetEditable(True)
            i += 1
        self.btn_edit.Hide()
        self.btn_save.Show()
        self.bounding_sizer.Layout()

    def save_edits(self, event):
        i = 0
        new_dict = {}
        new_dict.update({"_id": self.current_dataobj.id})
        new_dict.update({"_rev": self.current_dataobj.rev})
        for sizer_item in self.txtbox_sizer.__iter__():
            item = sizer_item.GetWindow()
            if i % 2 == 0:
                pass
            else:
                key = item.GetName()
                value = item.GetValue()
                kv_pair = {key: value}
                new_dict.update(kv_pair)
                item.SetEditable(False)
            i += 1
        self.hide_pw(event)
        self.btn_save.Hide()
        self.btn_edit.Show()
        self.btn_show_pw.Show()
        self.bounding_sizer.Layout()
        db_ops.DataBase.put(db, new_dict)
        print(new_dict)

    def show_pw(self, event):
        i = 0
        for sizer_item in self.txtbox_sizer.__iter__():
            if i % 2 == 0:
                pass
            else:
                ctrl = sizer_item.GetWindow()
                lbl = ctrl.GetName()
                if lbl == "password":
                    self.Freeze()
                    pw_ctrl = wx.TextCtrl(self, value=self.current_dataobj.password, style=wx.TE_READONLY)
                    pw_ctrl.SetName("password")
                    self.txtbox_sizer.Replace(ctrl, pw_ctrl)
                    ctrl.Hide()
                    ctrl.Destroy()
                    self.btn_show_pw.Hide()
                    self.btn_hide_pw.Show()
                    self.Parent.Refresh()
                    self.Parent.SendSizeEvent()
                    self.Thaw()
                    break
            i += 1

    def hide_pw(self, event):
        self.Freeze()
        self.set_style_pw()
        self.Parent.Refresh()
        self.Parent.SendSizeEvent()
        self.btn_hide_pw.Hide()
        self.btn_show_pw.Show()
        self.Thaw()

    def copy_pw(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.current_dataobj.password))
            wx.TheClipboard.Close()



if __name__ == "__main__":
    pass
