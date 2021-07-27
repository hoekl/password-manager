
from app.modules.db_manager import DataBase
from app.modules import steganography as steg
import time

password = "test"

class Lockout():
    def __init__(self):
        self.db = DataBase("lockout")

    def check_pw(self):
        if self.check_access() == True:
            pw = input("Password please:")
            if pw == password:
                self.clear_lockout()
                print("success")
            else:
                self.increase_count()
                if self.tries >= 5:
                    self.trigger_lockout()
                else:
                    self.check_pw()
        else:
            print("you're still timed out")

    def check_access(self):
        self.get_status()
        if self.tries < 5 or self.check_time() == True:
            return True
        elif self.tries >= 5 and self.check_time() == True:
            return True
        else:
            return False

    def get_status(self):
        res = self.db.query_all()
        if res["docs"] == []:
            tries = self._encode("5")
            time = self._encode("1")
            self.tries = 5
            self.time = 1
            self.db.db.put({"tries":tries, "time":time})
            self.get_status()
        else:
            doc = res["docs"][0]
            tries = doc["tries"]
            self.tries = int(self._decode(tries))
            self.id = doc["_id"]
            self.rev = doc["_rev"]
            try:
                time = doc["time"]
                self.time = float(self._decode(time))
            except:
                self.time = 1

    def increase_count(self):
        self.tries += 1
        self.update_db()
        self.get_status()

    def trigger_lockout(self):
        if self.tries == 5:
            self.lockout(30)
        if self.tries > 5:
            self.lockout(60)

        self.time = self.lockout_time
        self.update_db()

    def lockout(self, extratime):
        ctime = time.time()
        self.lockout_time = ctime + float(extratime)

    def clear_lockout(self):
        self.tries = 0
        self.time = 1
        self.update_db()

    def check_time(self):
        ctime = time.time()
        if ctime >= self.time:
            return True
        else:
            return False

    def update_db(self):
        tries = self._encode(self.tries)
        time = self._encode(self.time)
        self.db.db.put({"_id":self.id, "_rev":self.rev, "tries":tries, "time":time})

    def _encode(self, msg):
        byte_array = bytes(str(msg), "latin-1")
        length = len(byte_array)
        otp_array = steg.one_time_pad(length)
        xored = steg.encrypt_xor(otp_array, byte_array)
        binary_list = steg.convert_to_binary(xored)
        cover_text = steg.get_cover_text()
        merged_list = steg.merge_cover_with_secret(cover_text, binary_list)
        string_merged = "".join(merged_list)
        return string_merged

    def _decode(self, msg):
        bit_list = steg.decode_message(msg)
        otp_array = steg.one_time_pad((len(bit_list)//8))
        byte_str_list = steg.convert_to_bits(bit_list)
        byte_list = []
        byte_list = steg.split_to_bytes(byte_list,byte_str_list)
        binary_list = steg.string_bits_to_binary(byte_list)
        int_list = steg.binary_to_int(binary_list)
        decoded_msg = steg.decrypt_xor(otp_array, int_list)
        cleartext = steg.int_to_characters(decoded_msg)
        return cleartext

