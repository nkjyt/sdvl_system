from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase
import json, os

with open("firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",msg="")

    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['usr'] = email
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

@app.route("/remember", methods=['GET'])
def remember():
    usr = session.get('usr')
    return render_template("remember.html", usr=usr)

@app.route("/association", methods=['GET'])
def association():
    usr = session.get('usr')
    return render_template("association.html", usr=usr)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)