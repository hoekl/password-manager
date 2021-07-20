import pprint
import traceback
import couchdb2
import wx
from modules.configuration import config
from modules import encryption_handler as crypto

pp = pprint.PrettyPrinter(indent=4)
server = config.server()


class DataBase:
    def __init__(self, db_name) -> couchdb2.Database:
        if server.up() == True:
            try:
                self.db = server.get(
                    db_name, check=True
                )  # raises NotFoundError if database doesn't exist
                self.is_new = False
            except couchdb2.NotFoundError:
                self.db = server.create(db_name)
                self.is_new = True
        else:
            print("Server is not available")

    def set_fernet(self, fernet):
        self.fernet = fernet

    def get_logins_list(self):
        res = self.query_all()
        decrypted_docs = self.fernet.decrypt_initial(res)
        self.format_query_response(decrypted_docs)
        choices_list = list(self.id_dict.keys())

        return choices_list

    def query_all(self):
        self.check_is_db()
        selector = {"_id": {"$gt": None}}
        if self.db.exists() == True:
            res = self.db.find(selector, limit=1000)

        return res

    def get_doc_id(self, service_name):
        doc = self.id_dict.get(service_name)
        uID = doc["id"]

        return uID

    def get_doc_by_id(self, uID):
        encrypted_doc = self.db.get(uID, rev=None, revs_info=False, conflicts=False)
        doc = self.fernet.decrypt_individual(encrypted_doc)
        pp.pprint(doc)

        return doc

    def format_query_response(self, decrypted_docs):
        link_dict = {}
        for doc in decrypted_docs["doc_array"]:
            link_dict.update({doc["service name"]: {"id": doc["_id"]}})
        self.id_dict = link_dict

    def put(self, doc):
        encrypted_doc = self.fernet.encrypt_individual(doc)
        self.db.put(encrypted_doc)

    def delete(self, doc):
        self.db.delete(doc)

    def check_is_db(self):
        try:
            assert isinstance(self.db, couchdb2.Database)
        except Exception:
            print(traceback.print_exc())


class Fernet_obj:
    def __init__(self, fernet) -> crypto.Fernet:
        self.fernet = fernet

    def decrypt_initial(self, res):
        docs = {"doc_array": []}
        for doc in res["docs"]:
            doc_temp = {}
            for key, value in doc.items():
                if key != "_id" and key != "_rev":
                    d_key = self.fernet.decrypt(key.encode())
                    d_value = self.fernet.decrypt(value.encode())
                    strkey = d_key.decode()
                    strvalue = d_value.decode()
                    doc_temp.update({strkey: strvalue})
                elif key == "_id":
                    doc_temp.update({key: value})
            docs["doc_array"].append(doc_temp)
        return docs

    def decrypt_individual(self, doc):
        decrypted_doc = {}
        for key, value in doc.items():
            if key != "_id" and key != "_rev":
                d_key = self.fernet.decrypt(key.encode())
                d_value = self.fernet.decrypt(value.encode())
                strkey = d_key.decode()
                strvalue = d_value.decode()
                decrypted_doc.update({strkey: strvalue})
            else:
                decrypted_doc.update({key: value})

        return decrypted_doc

    def encrypt_individual(self, doc):
        encrypted_doc = {}
        for key, value in doc.items():
            if key == "_id" or key == "_rev":
                encrypted_doc.update({key: value})
            else:
                e_key = self.fernet.encrypt(key.encode())
                e_value = self.fernet.encrypt(value.encode())
                strkey = e_key.decode()
                strvalue = e_value.decode()
                encrypted_doc.update({strkey: strvalue})

        return encrypted_doc


class VerifyLogin(DataBase):
    def __init__(self, db_name) -> couchdb2.Database:
        super().__init__(db_name)

    def verify_password(self, password):
        key_manager = crypto.CryptoKeyManager(password)
        if self.verify(key_manager) == True:
            print("Password correct")
            return key_manager.fernet
        else:
            return False

    def verify(self, key_manager):
        res = self.query_all()
        for doc in res["docs"]:
            to_verify = doc["verify"]
        try:
            key_manager.decrypt(to_verify)
            return True
        except Exception:
            print("Invalid password")

    def setup(self, password):
        keymanager = crypto.CryptoKeyManager(password)
        crypto_message = keymanager.encrypt()
        v_doc = {"verify": crypto_message}
        self.db.put(v_doc)


class LoginData:
    def __init__(self, doc=None):
        if doc != None:
            self.id = doc.pop("_id")
            self.rev = doc.pop("_rev")
            self.data = doc
            try:
                self.password = doc["password"]
                self.password = doc["Password"]
            except:
                pass


if __name__ == "__main__":
    pass
