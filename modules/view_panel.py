import wx
import time
from modules import db_manager as db_ops

db = db_ops.DataBase("mock_data")


class ViewPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.number_of_fields = 0
        self.frame = parent
        self.txtbox_sizer = wx.GridBagSizer(0, 0)

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
                flag=wx.EXPAND | wx.BOTTOM,
                border=10,
            )
            self.number_of_fields += 2

        self.edit_button = wx.Button(self, label="Edit", size=(100, 50))
        self.edit_button.Bind(wx.EVT_BUTTON, self.set_editable)
        self.save_button = wx.Button(self, label="Save", size=(100, 50))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_edits)

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bounding_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.AddStretchSpacer()
        self.bounding_sizer.Add(self.txtbox_sizer, 3, wx.ALIGN_CENTER)
        self.bounding_sizer.Add(self.edit_button, 0, wx.ALIGN_CENTER, border=50)
        self.bounding_sizer.Add(self.save_button, 0, wx.ALIGN_CENTER, border=50)
        self.panel_sizer.Add(self.bounding_sizer, 3, wx.ALIGN_CENTER)
        self.panel_sizer.AddStretchSpacer()
        self.SetSizer(self.panel_sizer)
        self.save_button.Hide()
        self.Hide()

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

    def show_data(self, data_dict):
        self.Hide()
        tic = time.perf_counter()

        self.create_view(data_dict)

        toc = time.perf_counter()
        self.Show()
        self.frame.SendSizeEvent()
        print(f"Function executed in {toc-tic:0.4f} seconds")

    def create_view(self, data_dict):
        dict_length = len(data_dict) * 2
        if dict_length == self.number_of_fields:
            self.add_data_to_view(data_dict)
        elif dict_length > self.number_of_fields:
            self.add_field()
            self.create_view(data_dict)
        elif dict_length < self.number_of_fields:
            self.remove_field()
            self.create_view(data_dict)

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
                item.SetName(dict_keys[value_index])
                size = item.GetSizeFromText(text)
                item.SetMinSize(size)
                item.SetEditable(False)
                value_index += 1
            i += 1

    def set_editable(self, event):
        i = 0
        for sizer_item in self.txtbox_sizer.__iter__():
            item = sizer_item.GetWindow()
            if i % 2 == 0:
                pass
            else:
                item.SetEditable(True)
            i += 1
        self.edit_button.Hide()
        self.save_button.Show()
        self.bounding_sizer.Layout()

    def save_edits(self, event):
        i = 0
        new_dict = {}
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
        self.save_button.Hide()
        self.edit_button.Show()
        self.bounding_sizer.Layout()
        db_ops.DataBase.put(db, new_dict)
        print(new_dict)

    def evt_text(self, event):
        pass

    def evt_char(self, event):
        pass


if __name__ == "__main__":
    pass
