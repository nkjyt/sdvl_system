import pyrebase
import json

class Database():

    def __init__(self):
        with open("firebaseConfig.json") as f:
            firebaseConfig = json.loads(f.read())
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
    
    def read(self, UID):
        results = self.db.child("memorize").child(UID)
        print(results)
        return results