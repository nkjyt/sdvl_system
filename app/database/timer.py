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
        try:
            t = self.doc.get().to_dict()[dt]
            return self.hms(t)
        except:
            return "0h:00m:00s"
    
    def record_time(self):
        if self.start_d == datetime.date.today():
            t = time.time() - self.start_t
            if t > 60:
                t = 60
            dt = self.start_d.strftime('%Y-%m-%d')
            t_sum = self.doc.get().to_dict()[dt] + t
            self.doc.update({dt: t_sum})
        else:
            str_date = datetime.date.today().strftime('%Y-%m-%d')
            self.doc.update({str_date : 60.0})

        self.start_timer()