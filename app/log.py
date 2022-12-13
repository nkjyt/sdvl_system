import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import datetime, time

cred = credentials.Certificate("static/config/imp-sdvl-firebase-adminsdk-isaas-021c35f642.json")
firebase_admin.initialize_app(cred)

uid = "OTattFQ8vHf1iuPZv94sE3Gj3G22"
db = firestore.client()
doc = db.collection('time').document(uid)

# doc.update({"used" : str(now-start)})
start_t = ""
start_d = ""
docs = doc.get().to_dict()

def remove_decimals(input_str):
  # 小数点以下を削除するために、文字列を "." で分割します
  parts = input_str.split(".")
  # 小数点以下が存在しない場合は、そのまま返します
  if len(parts) == 1:
    return input_str
  # 小数点以下が存在する場合は、小数点以下を削除して返します
  else:
    return parts[0]

def deterimine_time(start):
    now = datetime.datetime.now()
    #1分以上は切り捨て
    if now.date() == start.date():
        print(remove_decimals(str(now - start)))
    else:
        print(now)

def start_timer():
    start_d = datetime.date(2022,12,12)
    return start_d ,time.time()

def record_time(start_d, start_t):
    if start_d == datetime.date.today():
        t = time.time() - start_t

        str_date = start_d.strftime('%Y-%m-%d')
        t_sum = docs[str_date] + t
        doc.update({str_date: t_sum})
    else:
        str_date = datetime.date.today().strftime('%Y-%m-%d')
        doc.update({str_date : 60.0})

def hms(td):
    m, s = divmod(td, 60)
    h, m = divmod(m, 60)
    return f"{h}h:{m}m:{s}s"


