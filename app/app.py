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

mdb = database.memorizeDB()
adb = database.associationDB()
jdb = database.japaneseDB()


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
    if request.method == 'GET':
        w = mdb.getUserWords(UID='OTattFQ8vHf1iuPZv94sE3Gj3G22')
        path = f'static/assets/{mdb.UID}/{mdb.eng}/{mdb.eng}'
        if w == '':
            return redirect(url_for('select'))
        return render_template("memorize.html", word = w, path=path)
    else:
        print(request.form['mode'].split(','))
        act, query = request.form['mode'].split(',')
        if act == "translate":
            if mdb.eng==query:
                w = mdb.jpn
            else:
                w = mdb.eng
        #rememberボタンを押したとき
        elif act == "next":
            if query == "remembered":
                mdb.remembered()
            else:
                mdb.notRemembered()
            if mdb.nextWord():
                w = mdb.eng
            else:
                return render_template("select.html")

        path = f'static/assets/{mdb.UID}/{mdb.eng}/{mdb.eng}'
        return render_template("memorize.html", word = w, path=path)

@app.route("/association", methods=['GET', 'POST'])
def association():
    data = {
        "eng" : "",
        "jpn" : "",
        "pos" : "",
        "hint" : "",
        "keywords" : [],
    }
    if request.method == 'GET':
        w = adb.getUserWords(UID='OTattFQ8vHf1iuPZv94sE3Gj3G22')
        if w == '':
            return redirect(url_for('select'))
        else:
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [word.replace(adb.eng+"_", "") for word in adb.imgName]
        return render_template("association.html", word = w, path=adb.imgName, data = data)
    else:
        adb.submit(request.form['answer'])
        if adb.nextWord():
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [word.replace(adb.eng+"_", "") for word in adb.imgName]
            return render_template("association.html", word = adb.eng, path=adb.imgName, data = data)
        else:
            return redirect(url_for('select'))

@app.route("/japanese", methods=['GET', 'POST'])
def japanese():
    if request.method == 'GET':
        w = jdb.getUserWords(UID='OTattFQ8vHf1iuPZv94sE3Gj3G22')
        if w == '':
                return redirect(url_for('select'))
        
        return render_template("japanese.html", word=w)
    else:
        print(request.form['mode'].split(','))
        act, query = request.form['mode'].split(',')
        if act == "translate":
            if jdb.eng==query:
                w = jdb.jpn
            else:
                w = jdb.eng
        #rememberボタンを押したとき
        elif act == "next":
            if query == "remembered":
                jdb.remembered()
            else:
                jdb.notRemembered()
            if jdb.nextWord():
                w = jdb.eng
            else:
                return render_template("select.html")

        # path = f'static/assets/{jdb.UID}/{jdb.eng}'
        return render_template("japanese.html", word = w)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)