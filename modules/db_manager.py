import couchdb2
import traceback
import pprint

pp = pprint.PrettyPrinter(indent=4)
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")


class DataBase():
    def __init__(self, dbName) -> couchdb2.Database:
        self.name = dbName
        if server.up() == True:
            try:
                self.db = server.get(self.name, check=True)     # raises NotFoundError if database doesn't exist
            except couchdb2.NotFoundError:
                self.dbCreate()


    def Create(self):
        if server.up() == True:
            try:
                self.db = server.create(self.name)
            except Exception:
                print(traceback.print_exc())


    def buildQuerySelector(self, querytype, querystring):
        if querytype == "search":
            self.selector = {
                "_id": {
                    "$gt": None
                },
                "$or": [
                    {"website": querystring},
                    {"service name": querystring}
                ]
            }


    def QueryAll(self):
        self.assertIsDB()
        self.selector = {
                "_id": {
                    "$gt": None
                }
            }

        if self.db.exists() == True:
            res = self.db.find(self.selector, limit=1000)
            #pp.pprint(res)

        return res


    def Query(self):
        self.assertIsDB()
        assert self.selector != None
        if self.db.exists() == True:
            res = self.db.find(self.selector)
            #pp.pprint(res)
        return res


    def assertIsDB(self):
        try:
            assert isinstance(self.db, couchdb2.Database)
        except Exception:
                print(traceback.print_exc())

if __name__ == "__main__":
    db = DataBase("mock_data")

