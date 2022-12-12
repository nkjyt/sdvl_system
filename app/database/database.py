import json, random, datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

class Initialize():

    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("static/config/imp-sdvl-firebase-adminsdk-isaas-021c35f642.json")
            firebase_admin.initialize_app(cred)

    def login(self, uid):
        self.uid = uid

class japaneseDB():

    def __init__(self):
        self.index = 0
        self.eng = ""
        self.jpn = ""
        self.data = []
        Initialize()
        self.db = firestore.client()
    
    def getUserWords(self, UID):
        if UID != "":
            self.UID = UID
        self.index = 0
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("japanese").document(UID)
            doc = doc_ref.get().to_dict()
            
            for word in doc.keys():
                if doc[word]['show']:
                    self.data.append(doc[word])
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
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            return True
        else:
            self.index = 0
            return False

    def remembered(self):
        self.data[self.index]['remembered'] += 1
        self.data[self.index]['show'] = False
        self.db.collection("japanese").document(self.UID).update({self.data[self.index]['word'] : self.data[self.index]})

    def notRemembered(self):
        self.data[self.index]['not_remembered'] += 1
        self.db.collection("japanese").document(self.UID).update({self.data[self.index]['word'] : self.data[self.index]})


class memorizeDB():

    def __init__(self):
        self.data = []
        self.index = 0
        self.imgurl = []
        Initialize()
        self.db = firestore.client()
    
    def getUserWords(self, UID):
        self.UID = UID
        self.index = 0
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("memorize").document(UID)
            doc = doc_ref.get().to_dict()

            for word in doc.keys():
                if doc[word]['show']:
                    self.data.append(doc[word])

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
        self.imgurl = self.data[self.index]['img']
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        print(self.data)

        return self.eng

    def nextWord(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            self.imgurl = self.data[self.index]['img']
            return True
        else:
            self.index = 0
            return False

    def remembered(self):
        self.data[self.index]['remembered'] += 1
        self.data[self.index]['show'] = False
        self.db.collection("memorize").document(self.UID).update({self.data[self.index]['word'] : self.data[self.index]})
        # self.db.child("memorize").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])
    
    def notRemembered(self):
        self.data[self.index]['not_remembered'] += 1
        self.db.collection("memorize").document(self.UID).update({self.data[self.index]['word'] : self.data[self.index]})
        # self.db.child("memorize").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])

class associationDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = []
        self.eng = ''
        self.jpn = ''
        self.pos = ''

    def getUserWords(self, UID):
        self.UID = UID
        self.index = 0
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("association").document(UID)
            doc = doc_ref.get().to_dict()

            for word in doc.keys():
                self.data.append(doc[word])
        if self.data == []:
            return ''

        random.shuffle(self.data)
        # for img in self.data[self.index]['img'].keys():
        #     self.imgurl.append(img)

        self.imgName = []
        self.imgurl = []
        for i in random.sample(self.data[self.index]['url'].keys(),3):
            self.imgName.append(i)
            self.imgurl.append(self.data[self.index]['url'][i])

        print(self.imgurl)
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        self.pos = self.data[self.index]['pos']

        return self.eng

    def nextWord(self):
        print(f"{self.index} : {self.eng}")
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            self.pos = self.data[self.index]['pos']
            # for img in self.data[self.index]['img'].keys():
            #     self.imgurl.append(img)
            self.imgName = []
            self.imgurl = []
            for i in random.sample(self.data[self.index]['url'].keys(),3):
                self.imgName.append(i)
                self.imgurl.append(self.data[self.index]['url'][i])
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
        try:
            self.data[self.index]['log'].update(up)
        except:
            self.data[self.index]['log'] = up
        
        self.db.collection("association").document(self.UID).update({self.data[self.index]['word'] : self.data[self.index]})
        # self.db.child("association").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])

# class japaneseDB():

#     def __init__(self):
#         with open("firebaseConfig.json") as f:
#             firebaseConfig = json.loads(f.read())
#         firebase = pyrebase.initialize_app(firebaseConfig)
#         self.db = firebase.database()
#         self.data = []
#         self.index = 0
    
#     def getUserWords(self, UID):
#         self.UID = UID
#         self.index = 0
#         if self.data == []:
#             print("データベースから初期化します")
#             for words in self.db.child("japanese").child(self.UID).get().each():
#                 if words.val()['show']:
#                     self.data.append(words.val())
#         else:
#             print("ローカルから読みこみます")
#             tmp = []
#             for i, v in enumerate(self.data):
#                 if self.data[i]['show']:
#                     tmp.append(v)
#             self.data = tmp
#         print(self.data)
#         if self.data == []:
#             return ''
#         random.shuffle(self.data)
#         self.eng = self.data[self.index]['word']
#         self.jpn = self.data[self.index]['jpn']
#         print(self.data)

#         return self.eng

#     def nextWord(self):
#         self.index += 1
#         if self.index < len(self.data):
#             self.eng = self.data[self.index]['word']
#             self.jpn = self.data[self.index]['jpn']
#             return True
#         else:
#             self.index = 0
#             return False

#     def remembered(self):
#         self.data[self.index]['remembered'] += 1
#         self.data[self.index]['show'] = False
#         self.db.child("japanese").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])

#     def notRemembered(self):
#         self.data[self.index]['not_remembered'] += 1
#         self.db.child("japanese").child(self.UID).child(self.data[self.index]['word']).update(self.data[self.index])
