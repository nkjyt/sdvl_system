import pyrebase
import json

class Database():

    def __init__(self):
        with open("firebaseConfig.json") as f:
            firebaseConfig = json.loads(f.read())
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
        self.memorize = None
    
    def read(self, UID):
        if self.memorize == None:
            self.memorize = self.db.child("memorize").child(UID)
        return self.memorize.get().val()