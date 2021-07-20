import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

base_path = os.path.abspath(os.path.dirname(__file__))


class CryptoKeyManager:
    def __init__(self, password):
        self.salt_path = self.get_path()
        try:
            self.salt = self.read_salt(self.salt_path)
            self.key = self.get_key(password)
            self.fernet = Fernet(self.key)
        except Exception:
                pass


    def get_path(self):
        data_dir = os.path.join(
            base_path, "configuration" + os.sep + "db_salt" + os.sep + "salt.key"
        )
        return data_dir

    def new_salt(self):
        return secrets.token_bytes(32)

    def import_salt(self, path_to_salt, password):
        self.salt = self.read_salt(path_to_salt)
        self.write_salt(self.salt)
        self.key = self.get_key(password)
        self.fernet = Fernet(self.key)

    def read_salt(self, path):
        with open(path, "rb") as f:
            salt = f.read()
        return salt

    def write_salt(self, salt):
        with open(self.salt_path, "wb") as f:
            f.write(salt)
        return salt

    def get_key(self, password):
        hashed = self.hash_input(password)
        key = self.derive_key(hashed)
        return key

    def hash_input(self, password):
        password = password.encode()
        pwhash = hashlib.sha256(password)
        return pwhash.hexdigest().encode()

    def derive_key(self, password):
        kdf = Scrypt(
            salt=self.salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self):
        message = "Password verification test"
        encrypted = self.fernet.encrypt(message.encode())
        return encrypted.decode()

    def decrypt(self, message):
        msg = message.encode()
        decrypted = self.fernet.decrypt(msg)
        return decrypted


if __name__ == "__main__":
    pass
