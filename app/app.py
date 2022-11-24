from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase
import json, os
import database.database as database

with open("firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = os.urandom(24)

db = database.Database()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",msg="")

    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['usr'] = email
        session['uid'] = auth.get_account_info(user['idToken'])['users'][0]['localId']
        return redirect(url_for('index'))
    except:
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('login'))
    return render_template("index.html", usr=usr)

@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('login'))

@app.route("/select", methods=['GET'])
def select():
    usr = session.get('usr')
    return render_template("select.html", usr=usr)

@app.route("/memorize", methods=['GET', 'POST'])
def memorize():
    #初期化
    data = db.read(UID='OTattFQ8vHf1iuPZv94sE3Gj3G22')

    eng = data[0]['word']
    jpn = data[0]['jpn']

    if request.method == 'GET':
        usr = session.get('usr')
        return render_template("memorize.html", word = eng)
    else:
        if eng==request.form['word']:
            w = jpn
        else:
            w = eng
        return render_template("memorize.html", word = w)

@app.route("/association", methods=['GET', 'POST'])
def association():
    eng = "ferocious"
    jpn = "獰猛な"
    if request.method == 'GET':
        usr = session.get('usr')
        return render_template("association.html", word = eng)
    else:
        if eng==request.form['word']:
            w = jpn
        else:
            w = eng
        return render_template("association.html", word = w)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)