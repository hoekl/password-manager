import unittest
import wx
import GUI as gui


class GUI_test(unittest.TestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.app.SetExitOnFrameDelete(True)
        self.app.MainLoop()

    def test_password(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")


        self.assertEqual(screen.check_pw("test"), True)
        self.assertEqual(screen.check_pw("t"), False)

    def test_create_newdb(self):
        screen = gui.LoginScreen(None, "test_new_db", "verification2")
        self.assertEqual(screen.existing_db_check(), False)    # False indicates user would like to set up new db
        screen.db.db.destroy()
        screen.verify_db.db.destroy()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GUI_test("test_password"))
    suite.addTest(GUI_test("test_create_newdb"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
