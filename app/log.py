import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("/app/static/config/imp-sdvl-firebase-adminsdk-isaas-021c35f642.json")
firebase_admin.initialize_app(cred)

res = firebase_admin.auth.get_user_by_email("test@gmail.com")
print(res.uid)