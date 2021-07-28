import unittest
# from unittest.case import TestCase
import time
import wx
import GUI as gui
from modules.encryption_handler import CryptoKeyManager


class GUI_test(unittest.TestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.app.SetExitOnFrameDelete(True)
        self.app.MainLoop()

    def test_correct_password(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")
        self.assertEqual(screen.check_pw("test"), True)

    def test_incorrect_password(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")
        self.assertEqual(screen.check_pw("t"), False)

    def test_create_newdb(self):
        self.salt = CryptoKeyManager("password").salt
        screen = gui.LoginScreen(None, "test_new_db", "verification2")
        self.assertEqual(screen.existing_db_check(), False)    # False indicates user would like to set up new db
        screen.key_manager.write_salt(self.salt)        #re-write overwritten salt
        screen.db.db.destroy()
        screen.verify_db.db.destroy()

    def test_fetch_speed(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")
        frame = gui.BaseFrame(None, title="Password Manager", db=screen.db)
        tic = time.perf_counter()
        frame.view_panel.list_box.SetSelection(0)
        toc = time.perf_counter()
        length_t = toc - tic
        self.assertLess(length_t, 0.5)

class CryptoKeyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.key_manager = CryptoKeyManager("password")

    def test_salt(self):
        self.assertEqual(isinstance(self.key_manager.read_salt(self.key_manager.salt_path), bytes), True)

    def test_create_new_salt(self):
        old_salt = self.key_manager.salt
        new_mnger = CryptoKeyManager("password", True)
        new_salt = new_mnger.salt
        self.assertNotEqual(old_salt, new_salt)
        new_mnger.write_salt(old_salt)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(GUI_test("test_correct_password"))
    suite.addTest(GUI_test("test_incorrect_password"))
    suite.addTest(GUI_test("test_create_newdb"))
    suite.addTest(GUI_test("test_fetch_speed"))
    suite.addTest(CryptoKeyTest("test_salt"))
    suite.addTest(CryptoKeyTest("test_create_new_salt"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
