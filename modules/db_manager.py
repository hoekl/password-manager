import couchdb2
import traceback

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
    if db.exists() == True:
        for id in db.ids():
            select = {"_id": id}
            res = db.find(select, limit=None,)
            print(res)

if __name__ == "__main__":
    dbName = "mock_data"
    db = dbConnect(dbName)
    if isinstance(db, couchdb2.Database) == True:
        pass
    else:
        db = dbCreate(dbName)
    dbQueryAll(db)
    res = db.get_indexes()
    print(res)


