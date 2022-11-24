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

class memorizeDB():

    def __init__(self):
        with open("firebaseConfig.json") as f:
            firebaseConfig = json.loads(f.read())
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
        self.data = None
        self.index = 0
    
    def getUserWords(self, UID):
        if self.data == None:
            self.data = self.db.child("memorize").child(UID).get().val()
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        print(self.data)

    def nextWord(self):
        if self.index < len(self.data) -1:
            self.index += 1
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            return True
        else:
            return False
