import wx
import time
from modules import db_manager as db_ops


dark_grey = wx.Colour(42, 42, 46)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(53, 53, 59)
grey_btn = wx.Colour(74, 74, 82)

class ViewPanel(wx.Panel):
    def __init__(self, *agrs, **kw):
        super().__init__(*agrs, **kw)
        self.number_of_fields = 0
        self.num_rmv_btns = 0
        self.SetBackgroundColour(dark_grey)
        self.txtbox_sizer = wx.BoxSizer(wx.VERTICAL)
        self.label_sizer = wx.BoxSizer(wx.VERTICAL)
        self.remove_btn_sizer = wx.BoxSizer(wx.VERTICAL)
        self.lbl_and_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.group_button_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bounding_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        while self.number_of_fields < 6:
            self.add_field()
            self.add_remove_btn()
            self.lbl_and_box_sizer.Hide(self.remove_btn_sizer)

        self.lbl_and_box_sizer.AddStretchSpacer()
        self.lbl_and_box_sizer.Add(
            self.label_sizer, 1, wx.EXPAND | wx.ALIGN_TOP, border=10
        )
        self.lbl_and_box_sizer.Add(
            self.txtbox_sizer, 1, wx.EXPAND | wx.ALIGN_TOP, border=10
        )
        self.lbl_and_box_sizer.Add(
            self.remove_btn_sizer,
            1,
            wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.EXPAND | wx.ALIGN_TOP,
        )
        self.lbl_and_box_sizer.AddStretchSpacer()

        self.bounding_sizer.Add(self.lbl_and_box_sizer, 3, wx.ALIGN_CENTER)

        self.btn_edit = wx.Button(
            self, label="Edit", size=(100, 50), style=wx.BORDER_NONE
        )
        self.btn_edit.Bind(wx.EVT_BUTTON, self.on_edit)
        self.btn_edit.SetBackgroundColour(grey_btn)
        self.btn_edit.SetForegroundColour(off_white)

        self.btn_save = wx.Button(
            self, label="Save", size=(100, 50), style=wx.BORDER_NONE
        )
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_edits)
        self.btn_save.Hide()
        self.btn_save.SetBackgroundColour(grey_btn)
        self.btn_save.SetForegroundColour(off_white)

        self.btn_show_pw = wx.Button(
            self, label="Show Password", size=(250, 50), style=wx.BORDER_NONE
        )
        self.btn_show_pw.Bind(wx.EVT_BUTTON, self.show_pw)
        self.btn_show_pw.Hide()
        self.btn_show_pw.SetBackgroundColour(grey_btn)
        self.btn_show_pw.SetForegroundColour(off_white)

        self.btn_hide_pw = wx.Button(
            self, label="Hide Password", size=(250, 50), style=wx.BORDER_NONE
        )
        self.btn_hide_pw.Bind(wx.EVT_BUTTON, self.hide_pw)
        self.btn_hide_pw.SetBackgroundColour(grey_btn)
        self.btn_hide_pw.SetForegroundColour(off_white)

        self.btn_copy_pw = wx.Button(
            self, label="Copy Password", size=(250, 50), style=wx.BORDER_NONE
        )
        self.btn_copy_pw.Bind(wx.EVT_BUTTON, self.copy_pw)
        self.btn_copy_pw.SetBackgroundColour(grey_btn)
        self.btn_copy_pw.SetForegroundColour(off_white)

        self.btn_delete_entry = wx.Button(
            self, label="Delete", size=(150, 50), style=wx.BORDER_NONE
        )
        self.btn_delete_entry.Bind(wx.EVT_BUTTON, self.on_delete)
        self.btn_delete_entry.SetBackgroundColour(grey_btn)
        self.btn_delete_entry.SetForegroundColour(off_white)

        self.btn_discard_edits = wx.Button(
            self, label="Discard Changes", size=(250, 50), style=wx.BORDER_NONE
        )
        self.btn_discard_edits.Bind(wx.EVT_BUTTON, self.discard_edits)
        self.btn_discard_edits.Hide()
        self.btn_discard_edits.SetBackgroundColour(grey_btn)
        self.btn_discard_edits.SetForegroundColour(off_white)

        self.btn_add_field = wx.Button(
            self, label="Add field", size=(250, 50), style=wx.BORDER_NONE
        )
        self.btn_add_field.Bind(wx.EVT_BUTTON, self.user_add_field)
        self.btn_add_field.Hide()
        self.btn_add_field.SetBackgroundColour(grey_btn)
        self.btn_add_field.SetForegroundColour(off_white)

        self.button_sizer1.Add(self.btn_edit, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer1.Add(self.btn_save, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer1.Add(25, 50)
        self.button_sizer1.Add(self.btn_discard_edits, 0, wx.ALIGN_CENTER, border=50)

        self.button_sizer1.Add(self.btn_show_pw, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer1.Add(self.btn_hide_pw, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer1.Add(25, 50)
        self.button_sizer1.Add(self.btn_copy_pw, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer1.Add(25, 50)
        self.button_sizer1.Add(self.btn_delete_entry, 0, wx.ALIGN_CENTER, border=50)

        self.button_sizer2.Add(
            self.btn_add_field,
            0,
            wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            border=50,
        )

        self.group_button_sizer.Add(self.button_sizer1, 0, wx.ALIGN_CENTER, border=50)
        self.group_button_sizer.Add(25, 25)
        self.group_button_sizer.Add(
            self.button_sizer2,
            0,
            wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            border=50,
        )

        self.bounding_sizer.Add(
            self.group_button_sizer,
            0,
            wx.ALIGN_CENTRE | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
        )

        self.panel_sizer.Add(
            self.bounding_sizer, 3, wx.ALIGN_CENTER | wx.RESERVE_SPACE_EVEN_IF_HIDDEN
        )

        self.SetSizer(self.panel_sizer)

    def add_field(self):
        self.number_of_fields += 1
        new_label = wx.StaticText(self)
        new_field = wx.TextCtrl(self)
        new_label.SetForegroundColour(off_white)
        new_field.SetForegroundColour(off_white)
        new_field.SetBackgroundColour(light_grey)
        self.label_sizer.Add(
            new_label,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )
        self.txtbox_sizer.Add(
            new_field,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )

    def remove_field(self):
        if self.label_sizer.GetChildren() and self.txtbox_sizer.GetChildren():
            sizer_item = self.label_sizer.GetItem(self.number_of_fields - 1)
            sizer_item2 = self.txtbox_sizer.GetItem(self.number_of_fields - 1)
            label = sizer_item.GetWindow()
            txtbox = sizer_item2.GetWindow()
            self.txtbox_sizer.Hide(label)
            self.txtbox_sizer.Hide(txtbox)
            label.Destroy()
            txtbox.Destroy()
            self.number_of_fields -= 1

    def user_add_field(self, event):
        self.number_of_fields += 1
        new_label = wx.TextCtrl(self)
        new_field = wx.TextCtrl(self)
        new_label.SetForegroundColour(off_white)
        new_field.SetForegroundColour(off_white)
        new_label.SetBackgroundColour(light_grey)
        new_field.SetBackgroundColour(light_grey)
        new_label.Bind(wx.EVT_KILL_FOCUS, self.set_field_name, new_label)
        self.label_sizer.Add(
            new_label,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )
        self.txtbox_sizer.Add(
            new_field,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )
        self.add_remove_btn()
        self.Parent.SendSizeEvent()

    def add_remove_btn(self):
        rmv_button = wx.Button(self, label="Remove", name=str(self.num_rmv_btns), style=wx.BORDER_NONE)
        rmv_button.Bind(wx.EVT_BUTTON, self.delete_field)
        rmv_button.SetBackgroundColour(grey_btn)
        rmv_button.SetForegroundColour(off_white)
        self.remove_btn_sizer.Add(
            rmv_button,
            1,
            flag=wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )
        self.num_rmv_btns += 1

    def del_remove_btn(self):
        if self.remove_btn_sizer.GetChildren():
            sizer_item = self.remove_btn_sizer.GetItem(self.num_rmv_btns - 1)
            btn = sizer_item.GetWindow()
            self.remove_btn_sizer.Hide(btn)
            btn.Destroy()
            self.num_rmv_btns -= 1

    def show_data(self, doc):
        self.btn_hide_pw.Hide()
        self.btn_copy_pw.Hide()
        self.btn_show_pw.Hide()
        self.btn_save.Hide()
        self.btn_discard_edits.Hide()
        self.btn_add_field.Hide()
        self.btn_edit.Show()
        tic = time.perf_counter()

        self.current_dataobj = db_ops.LoginData(doc)

        self.create_view(self.current_dataobj.data)

        toc = time.perf_counter()

        print(f"Function executed in {toc-tic:0.4f} seconds")

    def create_view(self, data_dict):
        dict_length = len(data_dict)
        if dict_length == self.number_of_fields:
            self.remove_pw_field()
            self.mng_remove_btns()
            self.lbl_and_box_sizer.Hide(self.remove_btn_sizer)
            self.convert_txtbox()
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
                temp_ctrl.SetBackgroundColour(light_grey)
                temp_ctrl.SetForegroundColour(off_white)
                self.txtbox_sizer.Replace(ctrl, temp_ctrl)
                ctrl.Destroy()

    def add_data_to_view(self, data_dict):
        panel_size = self.Parent.sizer.GetSize()
        size_x = panel_size[0] * 0.6
        key_index = 0
        value_index = 0
        dict_keys = list(data_dict.keys())
        dict_values = list(data_dict.values())

        for lblsizer_item in self.label_sizer.__iter__():
            label = lblsizer_item.GetWindow()
            label.SetLabel(dict_keys[key_index])
            key_index += 1

        for tbox_sizer_item in self.txtbox_sizer.__iter__():
            txtbox = tbox_sizer_item.GetWindow()
            box_content = dict_values[value_index]
            txtbox.SetLabel(box_content)
            txtbox.SetName(dict_keys[value_index])
            size_y = txtbox.GetBestHeight(size_x)
            new_size = (size_x, size_y)
            txtbox.SetMinSize(new_size)
            txtbox.SetEditable(False)
            value_index += 1

        self.set_style_pw()

    def set_style_pw(self):
        for item in self.txtbox_sizer.__iter__():
            ctrl = item.GetWindow()
            if ctrl.GetName() == "password":
                pw_ctrl = wx.TextCtrl(
                    self, value="abcdefg", style=wx.TE_READONLY | wx.TE_PASSWORD
                )
                pw_ctrl.SetForegroundColour(off_white)
                pw_ctrl.SetBackgroundColour(light_grey)
                pw_ctrl.SetName("password")
                self.txtbox_sizer.Hide(ctrl)
                self.txtbox_sizer.Replace(ctrl, pw_ctrl)
                ctrl.Destroy()
                self.btn_show_pw.Show()
                self.btn_copy_pw.Show()
                break

    def on_edit(self, event):
        self.Freeze()
        self.show_pw(event)
        self.btn_show_pw.Hide()
        self.btn_hide_pw.Hide()
        for sizer_item in self.txtbox_sizer.__iter__():
            txtbox = sizer_item.GetWindow()
            txtbox.SetEditable(True)
        self.convert_statictxt()
        self.lbl_and_box_sizer.Show(self.remove_btn_sizer)
        self.btn_edit.Hide()
        self.btn_save.Show()
        self.btn_discard_edits.Show()
        self.btn_add_field.Show()
        self.Layout()
        self.Thaw()

    def mng_remove_btns(self):
        if self.num_rmv_btns == self.number_of_fields:
            return
        if self.num_rmv_btns < self.number_of_fields:
            self.add_remove_btn()
            self.mng_remove_btns()
        if self.num_rmv_btns > self.number_of_fields:
            self.del_remove_btn()
            self.mng_remove_btns()

    def save_edits(self, event):
        new_doc = {}
        new_doc.update({"_id": self.current_dataobj.id})
        new_doc.update({"_rev": self.current_dataobj.rev})
        for sizer_item in self.txtbox_sizer.__iter__():
            txtbox = sizer_item.GetWindow()
            key = txtbox.GetName()
            value = txtbox.GetValue()
            if key == "" or value == "":
                pass
            else:
                new_doc.update({key: value})
            txtbox.SetEditable(False)

        self.hide_pw(event)
        self.btn_save.Hide()
        self.btn_edit.Show()
        self.btn_add_field.Hide()
        self.btn_discard_edits.Hide()
        self.bounding_sizer.Layout()
        db_ops.db.put(new_doc)
        self.Freeze()
        self.convert_txtbox()
        self.show_data(new_doc)
        self.Layout()
        self.Thaw()
        print(new_doc)

    def convert_txtbox(self):
        self.Freeze()
        for sizer_item in self.label_sizer.__iter__():
            item = sizer_item.GetWindow()
            if item.ClassName == "wxTextCtrl":
                value = item.Value
                static_text = wx.StaticText(self, label=value, style=wx.TE_READONLY)
                static_text.SetForegroundColour(off_white)
                self.label_sizer.Replace(item, static_text)
                item.Hide()
                item.Destroy()
        self.Parent.SendSizeEvent()
        self.Thaw()

    def convert_statictxt(self):
        self.Freeze()
        for sizer_item in self.label_sizer.__iter__():
            item = sizer_item.GetWindow()
            if item.ClassName == "wxStaticText":
                value = item.Label
                txtctrl = wx.TextCtrl(self, value=value)
                txtctrl.Bind(wx.EVT_KILL_FOCUS, self.set_field_name)
                txtctrl.SetBackgroundColour(light_grey)
                txtctrl.SetForegroundColour(off_white)
                self.label_sizer.Replace(item, txtctrl)
                item.Destroy()

        self.Parent.SendSizeEvent()
        self.Thaw()

    def show_pw(self, event):
        for sizer_item in self.txtbox_sizer.__iter__():
            ctrl = sizer_item.GetWindow()
            lbl = ctrl.GetName()
            if lbl == "password":
                self.Freeze()
                pw_ctrl = wx.TextCtrl(
                    self, value=self.current_dataobj.password, style=wx.TE_READONLY
                )
                pw_ctrl.SetBackgroundColour(light_grey)
                pw_ctrl.SetForegroundColour(off_white)
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

    def hide_pw(self, event):
        self.Freeze()
        self.set_style_pw()
        self.btn_hide_pw.Hide()
        self.btn_show_pw.Show()
        self.Parent.Refresh()
        self.Parent.SendSizeEvent()
        self.Thaw()

    def copy_pw(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.current_dataobj.password))
            wx.TheClipboard.Close()

    def discard_edits(self, event):
        self.Freeze()
        self.Parent.on_select_item(event)
        self.btn_discard_edits.Hide()
        self.btn_save.Hide()
        self.btn_add_field.Hide()
        self.btn_edit.Show()
        self.Layout()
        self.Thaw()

    def set_field_name(self, event):
        event.Skip()
        evt_source = event.EventObject
        label = evt_source.Label
        value = evt_source.Value
        children = self.txtbox_sizer.GetChildren()
        for sizer_child in children:
            txtbox = sizer_child.GetWindow()
            if txtbox.GetName() == label:
                txtbox.SetName(value)
                break

    def delete_field(self, event):
        self.Freeze()
        evt_source = event.EventObject
        index = int(evt_source.GetName())
        label_sizer = self.label_sizer.GetItem(index)
        txtbox_sizer = self.txtbox_sizer.GetItem(index)
        rmv_button_sizer = self.remove_btn_sizer.GetItem(index)
        label = label_sizer.GetWindow()
        txtbox = txtbox_sizer.GetWindow()
        rmv_button = rmv_button_sizer.GetWindow()
        self.label_sizer.Hide(label)
        self.txtbox_sizer.Hide(txtbox)
        self.remove_btn_sizer.Hide(rmv_button)
        label.Destroy()
        txtbox.Destroy()
        rmv_button.Destroy()
        self.num_rmv_btns -= 1
        self.number_of_fields -= 1
        self.Layout()
        self.Thaw()

    def on_delete(self, event):
        confirm_dialog = wx.MessageDialog(
            self,
            message="Are you sure you want to delete the selected item?",
            caption="Delete item?",
            style=wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT,
        )
        choice_response = confirm_dialog.ShowModal()
        confirm_dialog.Destroy()
        if choice_response == 5100:  # 5100 is response code for OK
            doc = {"_id": self.current_dataobj.id, "_rev": self.current_dataobj.rev}
            db_ops.db.delete(doc)

            # Get and display next item from list
            item_index = self.Parent.list_box.GetSelection()
            self.Parent.list_box.Delete(item_index)
            self.Parent.list_box.SetSelection(item_index)
            self.Parent.on_select_item(
                None  # passing None since function requires event
            )  # to be passed but event is not needed
            self.Parent.Update()


if __name__ == "__main__":
    pass
