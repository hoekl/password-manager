import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
base_path = os.path.abspath(os.path.dirname(__file__))

def get_path():
    data_dir = os.path.join(base_path, "secrets" + os.sep)
    return data_dir

def read_salt():
    path = os.path.join(get_path(), "salt.key")
    with open(path, "rb") as f:
        key = f.read()
    return key


def get_key(salt, password):
    hashed = hash_input(password)
    key = derive_key(salt, hashed)
    return key


def write_salt():
    salt = secrets.token_bytes(32)
    with open("salt.key", "wb") as f:
        f.write(salt)
    return salt


def hash_input(password):
    password = password.encode()
    pwhash = hashlib.sha256(password)
    return pwhash.hexdigest().encode()


def derive_key(salt, password):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt(message, key):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    with open("secretmsg.txt", "wb") as file:
        file.write(encrypted)


def read_encrypted():
    with open("secretmsg.txt", "rb") as file:
        encrypted = file.read()
    return encrypted


def decrypt(pw):
    salt = read_salt()
    password = hash_input(pw)
    key = derive_key(salt, password)
    f = Fernet(key)
    msg = read_encrypted()
    decrypted = f.decrypt(msg)
    print(decrypted)


if __name__ == "__main__":
    choice = input("1 to encrypt, 2 to decrypt:")
    if choice == "1":
        pw = input("Enter password to use:")
        salt = write_salt()
        key = get_key(salt, pw)
        message = input("Enter message to encrypt:")
        encrypt(message, key)

    if choice == "2":
        pw = input("Enter password to decrypt:")
        decrypt(pw)
