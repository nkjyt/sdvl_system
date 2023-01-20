import json, random, datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

class Initialize():

    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("static/config/sdvl-7ec02-firebase-adminsdk-xagyi-33dcbbc1b4.json")
            firebase_admin.initialize_app(cred)

    def login(self, uid):
        self.uid = uid
        print(f"login: {uid}")


class annotationDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = {}
        self.imgName = []
        self.eng = ''
        self.index = 0
        self.maxLen = 20

    
    def get_wordlist(self, uid):
        li = self.db.collection("settings").document(uid).get().to_dict()["wordlist"]
        return li
    
    def get_annotated_list(self, uid):
        try:
            dic = self.db.collection("annotation_log").document(uid).get().to_dict()
            li = dic.keys()
            li = [int(x) for x in li]
            return sorted(li)
        except:
            return []

    def get_data(self, UID, wordlist):
        self.UID = UID
        self.index = 0
        self.data = []
        self.wordlist = str(wordlist)
        try:
            self.log = self.db.collection("annotation_log").document(UID).to_dict()[self.wordlist]
        except:
            self.log = {}

        if self.data == []:
            doc_ref = self.db.collection("annotation_words").document(str(wordlist))
            doc = doc_ref.get().to_dict()
            words = doc['words']

            for word in words:
                word_data = self.db.collection("word_data").document(word).get().to_dict()
                self.data.append(word_data)

        print(f"words : {self.data[self.index]}")
        
        self.eng = self.data[self.index]['word']
        self.jpn = self.data[self.index]['jpn']
        self.defs = self.data[self.index]['definitions']
        self.imgurl = self.data[self.index]['url']
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            print(self.data[self.index])
            self.eng = self.data[self.index]['word']
            self.jpn = self.data[self.index]['jpn']
            self.defs = self.data[self.index]['definitions']
            self.imgurl = self.data[self.index]['url']
            return True
        else:
            self.index = 0
            return False

    def submit(self, word, feedback):
        self.log[word] = feedback
        try:
            self.db.collection("annotation_log").document(self.UID).update({self.wordlist : self.log})
        except:
            self.db.collection("annotation_log").document(self.UID).set({self.wordlist : self.log})

class learningDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.allurl = {}
        self.eng = ''
        self.isMatch = True
        self.index = 0
        self.maxLen = 100

    def get_img_url(self, urls, li):
        res = []
        for index in li:
            res.append(urls[index])
        return res

    def shuffle(self):
        print("shuffle")
        st = self.data[self.index]["set"]
        print(st)
        if st == "good":
            #正解
            print("正解")
            print(f"単語:{self.eng}, url:{self.allurl[self.eng]}")
            self.imgurl = random.choice(self.allurl[self.eng])
            self.isMatch = True
        else:
            #不正解
            print("不正解")
            self.imgurl = random.choice(random.choice(list(self.allurl.values())))
            print(f"選ばれたURL:{self.imgurl}")
            self.isMatch = False
            
    def get_data(self, UID, wordlist=""):
        self.UID = UID
        self.index = 0
        self.data = []

        if self.data == []:
            doc_ref = self.db.collection("learning_data").document(UID)
            doc = doc_ref.get().to_dict()
            words_good = doc['good_words']
            words_bad = doc['bad_words']

            for word, li in words_good.items():
                word_data = self.db.collection("word_data").document(word).get().to_dict()
                self.allurl[word] = self.get_img_url(word_data['url'], li)
                word_data["set"] = "good"
                self.data.append(word_data)
            for word in words_bad:
                word_data = self.db.collection("word_data").document(word).get().to_dict()
                word_data["set"] = "bad"
                self.data.append(word_data)
        
        random.shuffle(self.data)
        self.eng = self.data[self.index]['word']
        self.defs = self.data[self.index]['definitions']
        print(self.allurl)
        self.shuffle()
        self.maxLen = len(self.data)

        print(f"words : {self.data[self.index]}")
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.defs = self.data[self.index]['definitions']
            self.shuffle()
            return True
        else:
            self.index = 0
            return False
    
    def submit(self, answer):
        if answer=="True":
            ans = True
        else:
            ans = False
        data = {
            "answer" : ans,
            "isMatch" : self.isMatch,
            "word" : self.eng,
            "displayed_img" : self.imgurl
        }
        dt_now = datetime.datetime.now()
        stamp = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
        try:
            self.db.collection("learning_log").document(self.UID).update({stamp: data})
        except:
            self.db.collection("learning_log").document(self.UID).set({stamp: data})
    
    #正解不正解の判定
    def check_answer(self, answer):
        if answer=="True":
            ans = True
        else:
            ans = False
        if ans == self.isMatch:
            return True
        else:
            return False

class testDB():
    def __init__(self):
        Initialize()
        self.db = firestore.client()
        self.data = []
        self.index = 0
        self.imgurl = {}
        self.imgName = []
        self.eng = ''
        self.index = 0
        self.maxLen = 100
    
    def get_data(self, UID):
        self.UID = UID
        self.index = 0
        self.data = []
        if self.data == []:
            doc_ref = self.db.collection("test_data").document(UID).get().to_dict()
            self.data = doc_ref["test"]
        
        self.eng = self.data[self.index]["word"]
        self.defs = self.data[self.index]["definitions"]
    
    def next(self):
        self.index += 1
        if self.index < len(self.data):
            self.eng = self.data[self.index]['word']
            self.defs = self.data[self.index]['definitions']
            return True
        else:
            self.index = 0
            return False
    
    def submit(self, answer):
        if answer=="True":
            ans = True
        else:
            ans = False
        data = {
            "answer" : self.data[self.index]['answer'],
            "word" : self.eng,
            "defs" : self.defs,
            "user_ans" : ans
        }

        try:
            self.db.collection("test_log").document(self.UID).update({str(self.index): data})
        except:
            self.db.collection("test_log").document(self.UID).set({str(self.index): data})