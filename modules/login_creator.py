import secrets
import string
from couchdb2 import CouchDB2Exception
import wx
import hashlib
from modules import db_manager as db_ops
from modules import custom_widgets as cw

dark_grey = wx.Colour(38, 38, 38)
off_white = wx.Colour(235, 235, 235)
light_grey = wx.Colour(55, 55, 55)
grey_btn = wx.Colour(69, 69, 69)
edit_colour = wx.Colour(63, 63, 63)

class CreateLogin(wx.Panel):
    def __init__(self, *args, **kw):
        super(CreateLogin, self).__init__(*args, **kw)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.new_login_pnl = NewLogin(self)
        self.launch_dialog_btn = cw.Button(self, label="Generate Password")
        self.launch_dialog_btn.Bind(wx.EVT_BUTTON, self.on_generate)
        self.main_sizer.Add(self.new_login_pnl, 1, flag=wx.ALIGN_CENTER, border=50)
        self.main_sizer.Add(
            self.launch_dialog_btn, wx.SizerFlags().Centre().Border(wx.ALL, 5)
        )
        self.SetSizer(self.main_sizer)

    def on_generate(self, event):
        dialog = PWGenWindow(self, title="Generate new password")
        res = dialog.ShowModal()
        if res == 5100:
            password = dialog.txt_ctrl.Value
            self.new_login_pnl.autofill(password)
        else:
            pass
        dialog.Destroy()


    def on_refresh(self):
        self.new_login_pnl = NewLogin(self)
        self.new_login_pnl.SetBackgroundColour(dark_grey)
        self.new_login_pnl.SetForegroundColour(off_white)
        sizer_items = self.main_sizer.GetChildren()
        sizer_item = sizer_items[0]
        old_panel = sizer_item.GetWindow()
        self.Freeze()
        self.main_sizer.Replace(old_panel, self.new_login_pnl)
        old_panel.Destroy()
        self.main_sizer.Layout()
        self.Thaw()


class NewLogin(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.number_of_fields = 0
        self.num_rmv_btns = 0
        self.doc = {}
        self.label_sizer = wx.BoxSizer(wx.VERTICAL)
        self.txtbox_sizer = wx.BoxSizer(wx.VERTICAL)
        self.remove_btn_sizer = wx.BoxSizer(wx.VERTICAL)
        self.lbl_and_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bounding_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_save = cw.Button(self, label="Save")
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.button_sizer.Add(self.btn_save, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(25, 50)

        self.btn_add_field = cw.Button(self, label="Add field")
        self.btn_add_field.Bind(wx.EVT_BUTTON, self.add_custom_field)
        self.button_sizer.Add(self.btn_add_field, 0, wx.ALIGN_CENTER, border=50)
        self.button_sizer.Add(25, 50)

        self.btn_discard = cw.Button(self, label="Discard")
        self.btn_discard.Bind(wx.EVT_BUTTON, self.on_discard)
        self.button_sizer.Add(self.btn_discard, 0, wx.ALIGN_CENTER, border=50)

        default_choices = [
            "service name",
            "website",
            "email",
            "username",
            "password",
        ]

        while self.number_of_fields < 5:
            self.add_field(*default_choices)
            self.add_remove_btn()

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
        self.bounding_sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTER)

        self.panel_sizer.AddStretchSpacer()
        self.panel_sizer.Add(self.bounding_sizer, 3, wx.ALIGN_CENTER)
        self.panel_sizer.AddStretchSpacer()
        self.SetSizer(self.panel_sizer)

    def add_field(self, *default_choices):
        if default_choices:
            label_box = wx.TextCtrl(self, value=default_choices[self.number_of_fields], style=wx.BORDER_SIMPLE)
            txtbox = wx.TextCtrl(self, name=default_choices[self.number_of_fields], style=wx.BORDER_SIMPLE)
        else:
            label_box = wx.TextCtrl(self, name=str(self.number_of_fields), style=wx.BORDER_SIMPLE)
            txtbox = wx.TextCtrl(self, name=str(self.number_of_fields), style=wx.BORDER_SIMPLE)

        label_box.SetBackgroundColour(edit_colour)
        label_box.SetForegroundColour(off_white)
        txtbox.SetBackgroundColour(edit_colour)
        txtbox.SetForegroundColour(off_white)
        label_box.Bind(wx.EVT_KILL_FOCUS, self.txtctrl_on_focusloss)
        self.label_sizer.Add(
            label_box,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )
        self.txtbox_sizer.Add(
            txtbox,
            1,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_LEFT,
            border=10,
        )

        self.number_of_fields += 1

    def add_custom_field(self, event):
        self.add_field()
        self.add_remove_btn()
        self.Layout()

    def add_remove_btn(self):
        rmv_button = cw.Button(self, label="Remove", name=str(self.num_rmv_btns))
        rmv_button.Bind(wx.EVT_BUTTON, self.delete_field)
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
        i = 0
        for sizer_item in self.remove_btn_sizer.__iter__():
            ctrl = sizer_item.GetWindow()
            ctrl.SetName(str(i))
            i += 1

        self.Layout()
        self.Thaw()

    def txtctrl_on_focusloss(self, event):
        event.Skip()
        evt_source = event.EventObject
        label = evt_source.Name
        value = evt_source.Value
        children = self.txtbox_sizer.GetChildren()
        for sizer_child in children:
            txtbox = sizer_child.GetWindow()
            if txtbox.GetName() == label:
                txtbox.SetName(value)
                break

    def autofill(self, password):
        for sizer_item in self.txtbox_sizer.__iter__():
            txtbox = sizer_item.GetWindow()
            if txtbox.Name == "password":
                txtbox.SetValue(password)
                break

    def get_values(self):
        for sizer_item in self.txtbox_sizer.__iter__():
            ctrl = sizer_item.GetWindow()
            key = ctrl.GetName()
            value = ctrl.GetValue()
            if key == "" or value == "":
                pass
            else:
                self.doc.update({key: value})

    def create_UID(self):
        doc_hash = hashlib.sha256(str(self.doc).encode())
        hex_hash = doc_hash.hexdigest()
        str_hash = str(hex_hash)
        self.doc.update({"_id": str_hash})

    def on_save(self, event):
        self.get_values()
        if self.doc.values():
            self.create_UID()
            try:
                db_ops.db.put(self.doc)
                self.on_success()
                self.Parent.Parent.Parent.Parent.refresh()
                self.Parent.on_refresh()

            except CouchDB2Exception as db_except:
                print(db_except, "-Document already exists")
            except Exception as e:
                print(e)
        else:
            self.on_fail()

    def on_discard(self, event):
        dialog = wx.MessageDialog(
            self,
            message="Are you sure you want to clear the input?",
            caption="Warning!",
            style=wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT,
        )
        choice_response = dialog.ShowModal()
        if choice_response == 5100:
            self.Parent.on_refresh()
        dialog.Destroy()

    def on_success(self):
        dialog = wx.MessageDialog(
            self, message="Login saved successfully", caption="Success!", style=wx.OK
        )
        dialog.ShowModal()
        dialog.Destroy()

    def on_fail(self):
        dialog = wx.MessageDialog(
            self,
            message="Something went wrong. Please check your input is valid and try again",
            caption="Error",
            style=wx.OK,
        )
        dialog.ShowModal()
        dialog.Destroy()


class PWGenWindow(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetEscapeId(5101)
        self.pw_length = 24
        self.SetClientSize(self.FromDIP(wx.Size(500, 200)))
        self.generate_button = wx.Button(self, label="Generate Password")
        self.txt_ctrl = wx.TextCtrl(
            self,
            pos=(5, 5),
            size=(self.FromDIP(wx.Size(200, -1))),
            style=wx.TE_CENTRE,
        )
        self.spin_input = wx.SpinCtrl(
            self,
            style=wx.TE_PROCESS_ENTER,
            pos=(5, 15),
            min=8,
            max=32,
            initial=self.pw_length,
        )
        self.copy_button = wx.Button(self, label="Copy", size=(100, -1))
        self.autofill_button = wx.Button(self,id=wx.ID_OK, label="Use this password")
        self.choices_box = wx.CheckListBox(
            self,
            pos=(50, 50),
            choices=["Upper and Lowercase", "Digits", "Special Characters"],
        )
        self.choices_box.SetCheckedItems((0, 1, 2))
        self.generate_button.Bind(wx.EVT_BUTTON, self.generate_pw)
        self.copy_button.Bind(wx.EVT_BUTTON, self.copy_pw)
        self.spin_input.Bind(wx.EVT_SPINCTRL, self.set_pw_length)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sub_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sub_sizer1.Add(self.txt_ctrl, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.sub_sizer1.AddSpacer(10)
        self.sub_sizer1.Add(self.copy_button, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.sub_sizer2.Add(self.generate_button, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.sub_sizer2.AddSpacer(10)
        self.sub_sizer2.Add(self.spin_input, 0, flag=wx.ALIGN_CENTRE_VERTICAL)
        self.objects = [
            self.sub_sizer1,
            self.sub_sizer2,
            self.choices_box,
            self.autofill_button
        ]

        self.main_sizer.AddStretchSpacer()
        self.add_to_sizer(self.objects)
        self.main_sizer.AddStretchSpacer()
        self.SetSizer(self.main_sizer)

    def add_to_sizer(self, objects):
        for object in objects:
            self.main_sizer.Add(object, wx.SizerFlags().Centre().Border(wx.ALL, 15))

    def set_pw_length(self, event):
        self.pw_length = self.spin_input.GetValue()

    def set_pw_options(self, options):
        self.source_string = string.ascii_lowercase

        if 0 in options:
            self.source_string = string.ascii_letters
        if 1 in options:
            self.source_string += string.digits
        if 2 in options:
            self.source_string += string.punctuation

    def generate_pw(self, event):
        self.set_pw_options(self.choices_box.GetCheckedItems())
        password = "".join(
            (secrets.choice(self.source_string) for i in range(self.pw_length))
        )
        self.txt_ctrl.Clear()
        self.txt_ctrl.write(password)

    def copy_pw(self, event):
        self.txt_ctrl.SelectAll()
        self.txt_ctrl.Copy()

    def autofill(self, event):
        self.Destroy()



if __name__ == "__main__":
    pass
