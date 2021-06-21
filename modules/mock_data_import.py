import couchdb2
import json
import hashlib
server = couchdb2.Server("http://admin:pwmanager@127.0.0.1:5984")   # Arguments required according to local setup

def addTestData():
    try:
        db = server.create("mock_data")
    except couchdb2.CreationError:
        print("DB already exists")
        db = server.get("mock_data")


    with open("modules/MOCK_DATA.json") as f:
        mock = json.load(f)

    # Save each json object into its own document in the database
    for newDoc in mock:
        docHash = hashlib.sha256(str(newDoc).encode())      # get hash of json object to serve as
        hexHash = docHash.hexdigest()                       # unique ID to prevent duplicate entries
        strHash = str(hexHash)
        tempDict = {"_id": strHash}
        newDoc.update(tempDict)
        try:
            db.put(newDoc)
        except Exception as e:
            print(e, "-Document already exists")


addTestData()



# db.put_design("mydesign",
#               {"views":
#                {"name": {"map": "function (doc) {emit(doc.name, null);}"}
#                }
#               })
# result = db.view("mydesign", "name", key="another", include_docs=True)
# assert len(result) == 1
# print(result[0].doc)         # Same printout as above, using OrderedDict

# db.destroy()
