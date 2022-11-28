import pyrebase
import json, random, datetime

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
        if self.index < len(self.data) -1:
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



class associationDB():
    def __init__(self):
        with open("firebaseConfig.json") as f:
            firebaseConfig = json.loads(f.read())
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()
        self.data = []
        self.index = 0
        self.eng = ''
        self.jpn = ''
        self.pos = ''

    def getUserWords(self, UID):
        self.UID = UID
        self.index = 0
        self.imgName = []
        if self.data == []:
            print("データベースから初期化します")
            for words in self.db.child("association").child(self.UID).get().each():
                self.data.append(words.val())
        print(self.data)
        if self.data == []:
            return ''

        print(self.data[self.index]['img'])
        for img in self.data[self.index]['img'].keys():
            self.imgName.append(img)

        random.shuffle(self.data)
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        self.pos = self.data[self.index]['pos']

        return self.eng

    def nextWord(self):
        if self.index < len(self.data) -1:
            self.index += 1
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            return True
        else:
            self.index = 0
            return False

    def submit(self, answer):
        self.data[self.index]['count'] += 1
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        d = now.strftime('%Y%m%d%H%M%S')
        print(d)  # 20211104173728
        up = {
            d : {
                "img" : self.imgName,
                "answer" : answer
            }
        }
        print(up)

        """ self.data[self.index]['remembered'] += 1
        self.data[self.index]['show'] = False
        self.db.child("association").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index]) """
    
    def notRemembered(self):
        self.data[self.index]['not_remembered'] += 1
        self.db.child("association").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])
