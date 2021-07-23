
from modules.db_manager import DataBase
import time

password = "test"

class Lockout():
    def __init__(self):
        self.db = DataBase("lockout")

    def get_status(self):
        res = self.db.query_all()
        if res["docs"] == []:
            self.tries = 5
            lockout_time = self.lockout(300)
            self.db.db.put({"tries":5, "lockout":lockout_time})
        else:
            doc = res["docs"][0]
            self.tries = doc["tries"]
            self.id = doc["_id"]
            self.rev = doc["_rev"]
            try:
                self.time = doc["time"]
            except:
                self.time = 1

    def increase_count(self):
        self.tries += 1
        self.update_db()
        self.get_status()

    def trigger_lockout(self):
        if self.tries == 5:
            self.lockout(30)
        if self.tries > 5:
            self.lockout(60)

        self.time = self.lockout_time
        self.update_db()

    def lockout(self, extratime):
        ctime = time.time()
        self.lockout_time = ctime + float(extratime)

    def clear_lockout(self):
        self.tries = 0
        self.time = 1
        self.update_db()

    def check_time(self):
        ctime = time.time()
        if ctime >= self.time:
            return True
        else:
            return False

    def check_access(self):
        self.get_status()
        if self.tries < 5 or self.check_time() == True:
            return True
        elif self.tries >= 5 and self.check_time() == True:
            return True
        else:
            return False

    def update_db(self):
        self.db.db.put({"_id":self.id, "_rev":self.rev, "tries":self.tries, "time":self.time})

lock = Lockout()
def check_pw():
    if lock.check_access() == True:
        pw = input("Password please:")
        if pw == password:
            lock.clear_lockout()
            print("success")
        else:
            lock.increase_count()
            if lock.tries >= 5:
                lock.trigger_lockout()
            else:
                check_pw()
    else:
        print("you're still timed out")

check_pw()
