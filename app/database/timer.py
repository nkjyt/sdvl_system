import datetime, time
from firebase_admin import firestore

class Timer():

    def __init__(self):
        self.timer = ""
        self.db = firestore.client()
    
    def get_doc(self, uid):
        self.doc = self.db.collection('time').document(uid)

    def start_timer(self):
        self.start_d = datetime.date.today()
        self.start_t = time.time()
    
    def hms(self, td):
        m, s = divmod(td, 60)
        h, m = divmod(m, 60)
        return f"{int(h)}h:{int(m)}m:{int(s)}s"

    def get_time(self):
        dt = datetime.date.today().strftime('%Y-%m-%d')
        t = self.doc.get().to_dict()[dt]
        print(t)
        print(self.hms(t))
        try:
            t = self.doc.get().to_dict()[dt]
            return self.hms(t)
        except:
            return "0h:00m:00s"
    
    