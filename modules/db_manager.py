import couchdb2

server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")

def dbConnect(dbName):
    try:
        db = server.get(dbName)
        return db
    except Exception as e:
        try:
            db = server.create(dbName)
            return db
        except:
            print("Check database is accessible and try again")

db = dbConnect("mock_data")
assert isinstance(db, couchdb2.Database)

