import couchdb2
import traceback
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")


def dbConnect(dbName):
    if server.up() == True:
        try:
            db = couchdb2.Database(server, dbName, check=True)
        except Exception:
            print(traceback.print_exc())
        return db

def dbCreate(dbName):
    if server.up() == True:
        try:
            db = server.create(dbName)
        except Exception:
            print(traceback.print_exc())
        return db

def dbQueryAll(db):
    assert isinstance(db, couchdb2.Database)
    selector = {
            "_id": {
                "$gt": None
            }
        }

    if db.exists() == True:
        res = db.find(selector, limit=None)
        pp.pprint(res)
if __name__ == "__main__":
    dbName = "mock_data"
    db = dbConnect(dbName)
    if isinstance(db, couchdb2.Database) == True:
        pass
    else:
        db = dbCreate(dbName)
    dbQueryAll(db)



