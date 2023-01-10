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
        self.data = []
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("japanese").document(UID)
            doc = doc_ref.get().to_dict()
            
            for word in doc.keys():
                if doc[word]['show']:
                    self.data.append(doc[word])
        # else:
        #     print("ローカルから読みこみます")
        #     tmp = []
        #     for i, v in enumerate(self.data):
        #         if self.data[i]['show']:
        #             tmp.append(v)
        #     self.data = tmp
        
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

    def reset(self):
        print('reset')
        doc_ref = self.db.collection("japanese").document(self.UID)
        doc = doc_ref.get().to_dict()
            
        for word in doc.keys():

            doc[word]['show'] = True
            self.db.collection("japanese").document(self.UID).update({word: doc[word]})

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
        self.data = []
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("memorize").document(UID)
            doc = doc_ref.get().to_dict()

            for word in doc.keys():
                if doc[word]['show']:
                    self.data.append(doc[word])

        # else:
        #     print("ローカルから読みこみます")
        #     tmp = []
        #     for i, v in enumerate(self.data):
        #         if self.data[i]['show']:
        #             tmp.append(v)
        #     self.data = tmp
        print(self.data)
        if self.data == []:
            return ''
            
        self.imgurl = []
        for i in random.sample(self.data[self.index]['img'],3):
            self.imgurl.append(i)

        
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
            self.imgurl = []
            for i in random.sample(self.data[self.index]['img'],3):
                self.imgurl.append(i)

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

    def reset(self):
        print('reset')
        doc_ref = self.db.collection("memorize").document(self.UID)
        doc = doc_ref.get().to_dict()
            
        for word in doc.keys():

            doc[word]['show'] = True
            self.db.collection("memorize").document(self.UID).update({word: doc[word]})

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
                if doc[word]['show']:
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
    def reset(self):
        print('reset')
        doc_ref = self.db.collection("association").document(self.UID)
        doc = doc_ref.get().to_dict()
            
        for word in doc.keys():

            doc[word]['show'] = True
            self.db.collection("association").document(self.UID).update({word: doc[word]})

class feedbackDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = []
        self.eng = ''
        self.jpn = ''
        self.pos = ''
    
    def get_data(self, UID):
        self.UID = UID
        self.index = 0
        self.data = []
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("memorize").document(UID)
            doc = doc_ref.get().to_dict()

            for word in doc.keys():
                self.data.append(doc[word])

        if self.data == []:
            return ''
        
        self.imgurl = self.data[self.index]['img']
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
    

        return self.eng
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            self.imgurl = self.data[self.index]['img']
            return True
        else:
            self.index = 0
            return False

    def submit(self, fe, word):
        print(fe)
        # urlからファイル名を取っておく
        res = []
        for data in fe:
            f = data["url"].split("/")[-1]
            res.append({
                "url" : data["url"],
                "file" : f,
                "feedback" : data["feedback"]
            })
        self.db.collection("feedback").document(self.UID).update({word : res})

class feedback_associationDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = []
        self.imgName = []
        self.eng = ''
        self.defs = []
        self.pos = ''
    
    def get_data(self, UID):
        self.UID = UID
        self.index = 0
        self.data = []
        if self.data == []:
            print("データベースから初期化します")
            doc_ref = self.db.collection("association").document(UID)
            doc = doc_ref.get().to_dict()

            for word in doc.keys():
                self.data.append(doc[word])

        if self.data == []:
            return ''

        self.imgurl = []
        self.imgName = []
        for i in self.data[self.index]['url'].keys():
            self.imgName.append(" ".join(i.split("_")))
            self.imgurl.append(self.data[self.index]['url'][i])

        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
    

        return self.eng
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            self.imgurl = []
            self.imgName = []
            for i in self.data[self.index]['url'].keys():
                self.imgName.append(" ".join(i.split("_")))
                self.imgurl.append(self.data[self.index]['url'][i])
            return True
        else:
            self.index = 0
            return False

    def submit(self, fe, word):
        print(fe)
        # urlからファイル名を取っておく
        res = []
        for data in fe:
            f = data["url"].split("/")[-1]
            res.append({
                "url" : data["url"],
                "file" : f,
                "feedback" : data["feedback"]
            })
        print(res)
        # self.db.collection("feedback_association").document(self.UID).update({word : res})

class annotationDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = {}
        self.imgName = []
        self.eng = ''
        self.jpn = ''
        self.pos = ''
    
    def get_data(self, UID):
        self.UID = UID
        self.index = 0
        self.data = []

        if self.data == []:
            doc_ref = self.db.collection("annotation_words").document("000")
            doc = doc_ref.get().to_dict()
            words = doc['words']

            for word in words:
                word_data = self.db.collection("word_data").document(word).get().to_dict()
                self.data.append(word_data)

        print(f"words : {self.data[self.index]}")
        
        self.eng = self.data[self.index]['word']
        self.defs = self.data[self.index]['definitions']
        self.imgurl = self.data[self.index]['url']
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.defs = self.data[self.index]['definitions']
            self.imgurl = self.data[self.index]['url']
            return True
        else:
            self.index = 0
            return False

    def submit(self, word, feedback):
        try:
            self.db.collection("user").document(self.UID).update({word : feedback})
        except:
            self.db.collection("user").document(self.UID).set({word : feedback})