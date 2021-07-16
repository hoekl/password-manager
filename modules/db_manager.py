import pprint
import traceback
import couchdb2
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
            except couchdb2.NotFoundError:
                self.create_db(db_name)
        else:
            print("Server is not available")

    def create_db(self, db_name):
        if server.up() == True:
            try:
                self.db = server.create(db_name)
            except Exception:
                print(traceback.print_exc())
        else:
            print("Server is not available")

    def get_logins_list(self, password, salt):
        res = self.query_all()
        decrypted_docs = self.decrypt_initial(res, password, salt)
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
        doc = self.db.get(uID, rev=None, revs_info=False, conflicts=False)
        pp.pprint(doc)

        return doc

    def format_query_response(self, decrypted_docs):
        link_dict = {}
        for doc in decrypted_docs["doc_array"]:
            link_dict.update({doc["service name"]: {"id": doc["_id"]}})
        self.id_dict = link_dict

    def put(self, doc):
        self.db.put(doc)

    def delete(self, doc):
        self.db.delete(doc)

    def check_is_db(self):
        try:
            assert isinstance(self.db, couchdb2.Database)
        except Exception:
            print(traceback.print_exc())


    def decrypt_initial(self, res, password, salt):
        cryptokey = crypto.get_key(salt, password)
        f = crypto.Fernet(cryptokey)
        docs = {"doc_array":[]}
        for doc in res["docs"]:
            doc_temp = {}
            for key, value in doc.items():
                if key != "_id" and key != "_rev":
                    d_key = f.decrypt(key.encode())
                    d_value = f.decrypt(value.encode())
                    strkey = d_key.decode()
                    strvalue = d_value.decode()
                    doc_temp.update({strkey:strvalue})
                elif key == "_id":
                    doc_temp.update({key:value})
            docs["doc_array"].append(doc_temp)
        return docs

    def decrypt_individual(self, doc, password, salt):
        cryptokey = crypto.get_key(salt, password)
        f = crypto.Fernet(cryptokey)
        decrypted_doc = {}
        for key, value in doc.items():
            if key != "_id" and key != "_rev":
                d_key = f.decrypt(key.encode())
                d_value = f.decrypt(value.encode())
                strkey = d_key.decode()
                strvalue = d_value.decode()
                decrypted_doc.update({strkey:strvalue})
            else:
                decrypted_doc.update({key:value})

        return decrypted_doc


class VerifyLogin(DataBase):
    def __init__(self, db_name) -> couchdb2.Database:
        super().__init__(db_name)


    def verify(self, salt, password):
        res = self.query_all()
        for doc in res["docs"]:
            to_verify = doc["verify"]
        try:
            crypto.decrypt(salt, password, to_verify)
            return True
        except Exception:
            print("Invalid password")

    def setup(self):    # ! Modify to accept new string
        v_doc = {"verify": "gAAAAABg8YmgpdMUAEGvKjaKcDLZJmzLkHCxTJkyexDeB_FYLS7lGHpmyQlYj51UPsWMo8iEnLO1Nmla1oRLJA-6ixbEu7jQii3Jr-SsMVzG9mv_P-ddU8A="}
        self.put(v_doc)
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


db = DataBase("encrypted_mock_data")

def verify_password(password):
    db = VerifyLogin("verification")
    salt = crypto.read_salt()
    if db.verify(salt, password) == True:
        print("Password correct")
        return salt
    else:
        return False

if __name__ == "__main__":
    pass
