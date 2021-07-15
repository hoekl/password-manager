import couchdb2
import json
import hashlib
import encryption_handler as crypto
from secrets import config

salt = crypto.read_salt()

key = crypto.get_key(salt, config.password)
fernet = crypto.Fernet(key)

server = config.server()

def addTestData():
    try:
        db = server.create("encrypted_mock_data")
    except couchdb2.CreationError:
        print("DB already exists")
        db = server.get("encrypted_mock_data")

    with open("modules/MOCK_DATA.json") as f:
        mock = json.load(f)

    for doc in mock:
        new_doc = {}
        for key, value in doc.items():
            c_key = fernet.encrypt(key.encode()).decode()
            c_value = fernet.encrypt(value.encode()).decode()
            new_doc.update({c_key: c_value})
    # Save each json object into its own document in the database
        docHash = hashlib.sha256(
            str(new_doc).encode())     # get hash of json object to serve as
        hexHash = docHash.hexdigest()  # unique ID to prevent duplicate entries
        strHash = str(hexHash)
        new_doc.update({"_id": strHash})
        try:
            db.put(new_doc)
            print("success")
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
