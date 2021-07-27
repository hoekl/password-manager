import unittest
import wx
import GUI as gui

class GUI_test(unittest.TestCase):
    def setUp(self) -> None:
        app = wx.App()
        app.SetExitOnFrameDelete(True)
        self.screen = gui.LoginScreen(None)
        app.MainLoop()

    def test_password(self):
        self.assertEqual(self.screen.check_pw("test"), True)

if __name__ == "__main__":
    unittest.main()
