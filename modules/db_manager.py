import couchdb2
import traceback
import pprint

pp = pprint.PrettyPrinter(indent=4)
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")
dbName = "mock_data"

class DataBase():
    def __init__(self, dbName) -> couchdb2.Database:
        self.name = dbName
        if server.up() == True:
            try:
                self.db = server.get(self.name, check=True)     # raises NotFoundError if database doesn't exist
            except couchdb2.NotFoundError:
                self.dbCreate()


    def dbCreate(self):
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


    def dbQueryAll(self):
        self.assertIsDB()
        self.selector = {
                "_id": {
                    "$gt": None
                }
            }

        if self.db.exists() == True:
            res = self.db.find(selector, limit=None)
            pp.pprint(res)


    def dbQuery(self, selector):
        self.assertIsDB()
        assert selector != None
        if self.db.exists() == True:
            res = self.db.find(selector, limit=None)
            pp.pprint(res)


    def assertIsDB(self):
        try:
            assert isinstance(self.db, couchdb2.Database)
        except Exception:
                print(traceback.print_exc())

if __name__ == "__main__":
    db = DataBase(dbName)
    selector = db.buildQuerySelector("search", "laoreet")
    db.dbQuery(selector)
