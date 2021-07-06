import secrets
import string
import wx
import hashlib
from modules import db_manager as db_ops


class MainPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.new_login_pnl = NewLogin(self)
        self.launch_dialog_btn = wx.Button(self, label="Generate Password")
        self.launch_dialog_btn.Bind(wx.EVT_BUTTON, self.on_generate)
        self.main_sizer.Add(self.new_login_pnl, 1, flag=wx.ALIGN_CENTER, border=50)
        self.main_sizer.Add(
            self.launch_dialog_btn, wx.SizerFlags().Centre().Border(wx.ALL, 5)
        )
        self.SetSizer(self.main_sizer)

    def on_generate(self, event):
        dialog = PWGenWindow()
        dialog.ShowModal()
        dialog.Destroy()


class NewLogin(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.number_of_fields = 0
        self.txtbox_sizer = wx.GridBagSizer(0, 0)
        self.bounding_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_save = wx.Button(self, label="Save")
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.button_sizer.Add(self.btn_save, 0, wx.ALIGN_CENTER, border=50)
        default_choices = ["service name", "website", "email", "username", "password"]

        while self.number_of_fields < 5:
            label_box = wx.TextCtrl(self, value=default_choices[self.number_of_fields])
            field_box = wx.TextCtrl(self, name=default_choices[self.number_of_fields])
            self.txtbox_sizer.Add(
                label_box,
                pos=(self.number_of_fields, 0),
                flag=(wx.EXPAND | wx.ALL),
                border=10,
            )
            self.txtbox_sizer.Add(
                field_box,
                pos=(self.number_of_fields, 1),
                flag=(wx.EXPAND | wx.ALL),
                border=10,
            )

            self.number_of_fields += 1

        self.panel_sizer.AddStretchSpacer()
        self.bounding_sizer.Add(self.txtbox_sizer, 3, wx.ALIGN_CENTER)
        self.bounding_sizer.Add(self.button_sizer, 0, wx.ALIGN_CENTER)
        self.panel_sizer.Add(self.bounding_sizer, 3, wx.ALIGN_CENTER)
        self.panel_sizer.AddStretchSpacer()
        self.SetSizer(self.panel_sizer)

    def on_save(self, event):
        i = 0
        doc = {}
        for sizer_item in self.txtbox_sizer.__iter__():
            if i % 2 == 0:
                pass
            else:
                ctrl = sizer_item.GetWindow()
                key = ctrl.GetName()
                value = ctrl.GetValue()
                if key == None or value == None:
                    pass
                else:
                    doc.update({key: value})
            i += 1
        if doc:
            doc_hash = hashlib.sha256(str(doc).encode())
            hex_hash = doc_hash.hexdigest()
            str_hash = str(hex_hash)
            doc.update({"_id": str_hash})
            print(doc, str_hash)
            try:
                db_ops.db.put(doc)
                self.Parent.Refresh
            except Exception as e:
                print(e, "-Document already exists")
        else:
            print("Fields can't be empty")


class PWGenWindow(wx.Dialog):
    def __init__(self):
        super().__init__(parent=None, title="Generate new password")
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
        self.copy_button = wx.Button(self, label="Copy", size=(100, 50))
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


if __name__ == "__main__":
    pass
