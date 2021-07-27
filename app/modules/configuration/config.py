import couchdb2

def server():
    server = couchdb2.Server(
        "http://admin:pwmanager@127.0.0.1:5984"
    )
    return server

password = "test"

if __name__ == "__main__":
    pass
