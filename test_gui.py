import unittest
import time
import wx
import GUI as gui
from modules.encryption_handler import CryptoKeyManager
import lockout_manager
from modules.custom_widgets import PWStrengthIndicator, StrengthSizer


class GUI_test(unittest.TestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        wx.Log.SetActiveTarget(wx.LogStderr())
        self.frame = wx.Frame(None, title='WTC: '+self.__class__.__name__)
        self.frame.Show()
        self.frame.PostSizeEvent()

    def tearDown(self):
        def _cleanup():
            for tlw in wx.GetTopLevelWindows():
                if tlw:
                    if isinstance(tlw, wx.Dialog) and tlw.IsModal():
                        tlw.EndModal(0)
                        wx.CallAfter(tlw.Destroy)
                    else:
                        tlw.Close(force=True)
            wx.WakeUpIdle()

        timer = wx.PyTimer(_cleanup)
        timer.Start(100)
        self.app.MainLoop()
        del self.app

    def test_correct_password(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")
        self.assertEqual(screen.check_pw("test"), True)

    def test_incorrect_password(self):
        screen = gui.LoginScreen(None, "mock_data", "verification")
        self.assertEqual(screen.check_pw("t"), False)

    def test_create_newdb(self):
        self.salt = CryptoKeyManager("password").salt
        screen = gui.LoginScreen(None, "test_new_db", "verification2")
        self.assertEqual(
            screen.existing_db_check(), False
        )  # False indicates user would like to set up new db
        screen.key_manager.write_salt(self.salt)  # re-write overwritten salt
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

    def test_advice(self):
        self.sizer = StrengthSizer(self.frame, c_style=None)
        self.indicator = self.sizer.strengthbar
        self.indicator.set_pw("aaaaaaaaaaaa")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using a longer password, uppercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaaa")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaaA")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaA1")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaA1!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "")
        self.indicator.set_pw("aaaaaaaaaaa1!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaa!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters and numbers for extra security.")
        self.indicator.set_pw("AAAAAAAAAAAAA")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("1234567891011")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters, uppercase characters and special characters for extra security.")
        self.indicator.set_pw("1234567891011!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters and uppercase characters for extra security.")
        self.indicator.set_pw(None)


    def test_strength_calculator(self):
        self.sizer = StrengthSizer(self.frame, c_style=None)
        self.indicator = self.sizer.strengthbar
        self.indicator.set_pw("£")
        self.assertGreaterEqual(self.indicator.calc_strength(), 1)
        self.indicator.set_pw("aaaaaaaaaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 20)
        self.indicator.set_pw("aaaaaaaaaaaa1")
        self.assertGreaterEqual(self.indicator.calc_strength(), 30)
        self.indicator.set_pw("aaaaaaaaaaaa1!")
        self.assertGreaterEqual(self.indicator.calc_strength(), 40)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 50)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaaaaaaaaaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 70)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaaaaaaaaaa!!AAAAAA")
        self.assertGreaterEqual(self.indicator.calc_strength(), 90)
        self.indicator.set_pw(None)


class CryptoKeyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.key_manager = CryptoKeyManager("password")

    def test_salt(self):
        self.assertEqual(
            isinstance(self.key_manager.read_salt(self.key_manager.salt_path), bytes),
            True,
        )

    def test_create_new_salt(self):
        old_salt = self.key_manager.salt
        new_mnger = CryptoKeyManager("password", True)
        new_salt = new_mnger.salt
        self.assertNotEqual(old_salt, new_salt)
        new_mnger.write_salt(old_salt)


class LockoutTest(unittest.TestCase):
    def setUp(self) -> None:
        self.lockout = lockout_manager.Lockout("test_lockout")

    def test_right_pw(self):
        self.assertEqual(self.lockout.check_pw("testing"), True)
        self.assertEqual(self.lockout.check_access(), True)

    def test_wrong_pw(self):
        """Enters incorrect password 5 times, should result in 30 second timeout"""
        i = 1
        while i < 5:
            self.assertEqual(self.lockout.check_pw("jhkgfgfh"), False)
            self.assertEqual(self.lockout.check_access(), True)
            i += 1

        self.assertEqual(self.lockout.check_pw("jhkgfgfh"), False)
        self.assertEqual(self.lockout.check_access(), False)

    def test_clear_lockout(self):
        """Continues from previous test, will wait for timeout to finish, then enter
        correct password to clear lockout"""
        self.assertEqual(self.lockout.check_access(), False)
        time.sleep(30)
        self.assertEqual(self.lockout.check_pw("testing"), True)
        self.assertEqual(self.lockout.check_access(), True)
        print("")


class PasswordStrengthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.app.MainLoop()
        frame = wx.Frame()
        self.indicator = PWStrengthIndicator(frame, password=None, c_style=None)

    def test_advice(self):
        self.indicator.set_pw("aaaaaaaaaaaa")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using a longer password, uppercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaaa")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaaA")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using numbers and special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaA1")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using special characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaA1!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "")
        self.indicator.set_pw("aaaaaaaaaaa1!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters for extra security.")
        self.indicator.set_pw("aaaaaaaaaaaa!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using uppercase characters and numbers for extra security.")
        self.indicator.set_pw("AAAAAAAAAAAAA")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters, numbers and special characters for extra security.")
        self.indicator.set_pw("1234567891011")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters, uppercase characters and special characters for extra security.")
        self.indicator.set_pw("1234567891011!")
        self.indicator.calc_strength()
        self.assertEqual(self.indicator.advice, "Consider using lowercase characters and uppercase characters for extra security.")

    def test_strength_calculator(self):
        self.indicator.set_pw("£")
        self.assertGreaterEqual(self.indicator.calc_strength(), 1)
        self.indicator.set_pw("aaaaaaaaaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 20)
        self.indicator.set_pw("aaaaaaaaaaaa1")
        self.assertGreaterEqual(self.indicator.calc_strength(), 30)
        self.indicator.set_pw("aaaaaaaaaaaa1!")
        self.assertGreaterEqual(self.indicator.calc_strength(), 40)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 50)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaaaaaaaaaa")
        self.assertGreaterEqual(self.indicator.calc_strength(), 70)
        self.indicator.set_pw("aaaaaaaaaaaa1!Aaaaaaaaaaa!!AAAAAA")
        self.assertGreaterEqual(self.indicator.calc_strength(), 90)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(GUI_test("test_correct_password"))
    suite.addTest(GUI_test("test_incorrect_password"))
    suite.addTest(GUI_test("test_create_newdb"))
    suite.addTest(GUI_test("test_fetch_speed"))
    suite.addTest(GUI_test("test_advice"))
    suite.addTest(GUI_test("test_strength_calculator"))
    suite.addTest(CryptoKeyTest("test_salt"))
    suite.addTest(CryptoKeyTest("test_create_new_salt"))
    suite.addTest(LockoutTest("test_right_pw"))
    suite.addTest(LockoutTest("test_wrong_pw"))
    suite.addTest(LockoutTest("test_clear_lockout"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
