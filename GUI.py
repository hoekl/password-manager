import wx

from modules import login_creator as login

class BaseFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(BaseFrame, self).__init__(*args, **kw)

        noteBookPanel = wx.Notebook(self)
        firstPanel = login.MainPanel(noteBookPanel)     #implement own class to add functionality
        secondPanel = wx.Panel(noteBookPanel)
        noteBookPanel.AddPage(firstPanel, "New Login", True)
        noteBookPanel.AddPage(secondPanel, "Logins", True)



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = BaseFrame(None, title='Password Manager')
    frm.Show()
    app.MainLoop()
