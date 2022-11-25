import pyrebase
import json
import random

class Database():
  
    def __init__(self):
        with open("firebaseConfig.json") as f:
            firebaseConfig = json.loads(f.read())
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
        self.memorize = None
        self.UID = ''
    
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
        self.data = []
        self.index = 0
    
    def getUserWords(self, UID):
        self.UID = UID
        self.index = 0
        if self.data == []:
            print("データベースから初期化します")
            for words in self.db.child("memorize").child(self.UID).get().each():
                if words.val()['show']:
                    self.data.append(words.val())
        else:
            print("ローカルから読みこみます")
            tmp = []
            for i, v in enumerate(self.data):
                if self.data[i]['show']:
                    tmp.append(v)
            self.data = tmp
        print(self.data)
        if self.data == []:
            return ''
        random.shuffle(self.data)
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        print(self.data)

        return self.eng

    def nextWord(self):
        print(f"{self.index}番目：最大{len(self.data)}")
        if self.index < len(self.data) -1:
            print(f"{self.index}番目：最大{len(self.data)}")
            self.index += 1
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            return True
        else:
            self.index = 0
            return False

    def remembered(self):
        self.data[self.index]['remembered'] += 1
        self.data[self.index]['show'] = False
        self.db.child("memorize").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])
    
    def notRemembered(self):
        self.data[self.index]['not_remembered'] += 1
        self.db.child("memorize").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])