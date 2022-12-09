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
ini = database.Initialize()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",msg="")

    email = request.form['email']
    password = request.form['password']
    try:
        # user = firebase_admin.auth.get_user_by_email(email)
        # ini.login(user.uid)
        user = auth.sign_in_with_email_and_password(email, password)
        ini.login(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        return redirect(url_for('select'))
    except:
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")
@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:
        return redirect(url_for('login'))
    return render_template("login.html", usr=usr)

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
        w = mdb.getUserWords(ini.uid)
        if w == '':
            return redirect(url_for('select'))
        return render_template("memorize.html", word = w, path=mdb.imgurl)
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

        return render_template("memorize.html", word = w, path=mdb.imgurl)

#フラッシュカードを裏返した時の処理
@app.route("/memorize#card", methods=['POST'])
def memorize_card():
    act, query = request.form['mode'].split(',')
    if act == "translate":
            if mdb.eng==query:
                w = mdb.jpn
            else:
                w = mdb.eng
    return render_template("memorize.html", word= w, path=mdb.imgurl)

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
        w = adb.getUserWords(ini.uid)
        if w == '':
            return redirect(url_for('select'))
        else:
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [word.replace(adb.eng+"_", "") for word in adb.imgName]
        return render_template("association.html", word = w, path=adb.imgurl, data = data)
    else:
        # adb.submit(request.form['answer'])
        if adb.nextWord():
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [word.replace(adb.eng+"_", "") for word in adb.imgName]
            return render_template("association.html", word = adb.eng, path=adb.imgurl, data = data)
        else:
            return redirect(url_for('select'))

@app.route("/association/answer", methods=['POST'])
def post_answer():
    data = {}
    answer = request.form['answer']
    adb.submit(answer)
    if answer == adb.eng:
        msg = "正解！"
    else:
        msg = "不正解"
    data['eng'] = adb.eng
    data['jpn'] = adb.jpn
    data['answer'] = request.form['answer']
    data["keywords"] = [word.replace(adb.eng+"_", "") for word in adb.imgName]
    return render_template("association_answer.html",path=adb.imgurl, data = data, msg = msg)

@app.route("/japanese", methods=['GET', 'POST'])
def japanese():
    if request.method == 'GET':
        w = jdb.getUserWords(ini.uid)
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
    app.run(host="0.0.0.0", port=80,debug=True)