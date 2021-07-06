import pprint
import traceback

import couchdb2

pp = pprint.PrettyPrinter(indent=4)
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")



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

    def get_logins_list(self):
        res = self.query_all()
        self.format_query_response(res)
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

    def format_query_response(self, res):
        link_dict = {}
        for doc in res["docs"]:
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

class LoginData:
    def __init__(self, doc=None):
        if doc != None:
            self.id = doc.pop("_id")
            self.rev = doc.pop("_rev")
            self.data = doc
            self.password = doc["password"]

db = DataBase("copy_mock_data")

if __name__ == "__main__":
    pass
