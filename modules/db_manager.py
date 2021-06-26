import pprint
import traceback

import couchdb2

pp = pprint.PrettyPrinter(indent=4)
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")


class DataBase:
    def __init__(self, dbName) -> couchdb2.Database:
        self.name = dbName
        if server.up() == True:
            try:
                self.db = server.get(
                    self.name, check=True
                )  # raises NotFoundError if database doesn't exist
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
                "_id": {"$gt": None},
                "$or": [{"website": querystring}, {"service name": querystring}],
            }

    def QueryAll(self):
        self.assertIsDB()
        self.selector = {"_id": {"$gt": None}}

        if self.db.exists() == True:
            res = self.db.find(self.selector, limit=1000)
            # pp.pprint(res)
        return res

    def Query(self):
        self.assertIsDB()
        assert self.selector != None
        if self.db.exists() == True:
            res = self.db.find(self.selector)
            # pp.pprint(res)
        return res

    def formatQueryRes(self, res):
        link_dict = {}
        for doc in res["docs"]:
            link_dict.update(
                {
                    doc["service name"]: {
                        "id": doc["_id"],
                        "website": doc["website"],
                    }
                }
            )
        #pp.pprint(link_dict)
        self.linkDict = link_dict

    def getIDfromDict(self, serviceName):
        doc = self.linkDict.get(serviceName)
        uID = doc["id"]
        return uID

    def getDocByID(self, uID):
        doc = self.db.get(uID, rev=None, revs_info=False, conflicts=False)
        pp.pprint(doc)
        return doc

    def assertIsDB(self):
        try:
            assert isinstance(self.db, couchdb2.Database)
        except Exception:
            print(traceback.print_exc())


if __name__ == "__main__":
    db = DataBase("mock_data")
    res = db.QueryAll()
    link_dict = db.formatQueryRes(res)
    uID = db.getIDfromDict(link_dict, "aliquam")
    pp.pprint(db.getDocByID(uID))
    print(uID)
