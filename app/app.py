from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase
import json, os, re
import database.database as database
import database.timer as f_timer

with open("firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = os.urandom(24)

# mdb = database.memorizeDB()
# adb = database.associationDB()
# jdb = database.japaneseDB()
# fdb = database.feedbackDB()
# fadb = database.feedback_associationDB()
andb = database.annotationDB()
ldb = database.learningDB()
tdb = database.testDB()
ini = database.Initialize()
timer = f_timer.Timer()

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
        uid = auth.get_account_info(user['idToken'])['users'][0]['localId']
        ini.login(uid)
        timer.get_doc(uid)
        return redirect(url_for('select'))
    except:
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
    try:
        uid = ini.uid
        if uid == "":
            return redirect(url_for('login'))
        return render_template("login.html", usr=uid)
    except:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('login'))

@app.route("/select", methods=['GET'])
def select():
    try:
        uid = ini.uid
        print(uid)
        t = timer.get_time()
        return render_template("select.html", usr=uid, time_log=t)
    except:
        return redirect(url_for('login'))

@app.route("/annotation", methods=["GET", "POST"])
def annotaion():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))

    if request.method == "GET":
        wordlist = request.args.get('wordlist', "")
        print(wordlist)
        andb.get_data(uid, wordlist)
        timer.start_timer()
        return render_template("annotation.html", word=andb.eng, defs=andb.defs,
         path=andb.imgurl, isTrans=False, maxLen=andb.maxLen, idx=andb.index+1)
    else:
        try:
            feedback = []
            for i in range(3):
                key = "img" + str(i)
                feedback.append(request.form[key])
            andb.submit(andb.eng, feedback)
        except:
            print("not selected")
        if not andb.next():
            return redirect(url_for("select"))
        
        return render_template("annotation.html", word=andb.eng, defs=andb.defs, path=andb.imgurl,
         isTrans=False, maxLen=andb.maxLen, idx=andb.index+1)

@app.route("/annotation/translate", methods=["GET", "POST"])
def annotation_translate():

    return render_template("annotation.html", word=andb.eng, defs=andb.defs, path=andb.imgurl,
     isTrans=True, jpn=andb.jpn,  maxLen=andb.maxLen, idx=andb.index+1)

@app.route("/select/wordset", methods=["GET", "POST"])
def select_wordset():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    li = andb.get_wordlist(uid)
    annotated = andb.get_annotated_list(uid)
    return render_template("select_wordset.html", index_list=li, annotated=annotated)

@app.route("/learning", methods=["GET", "POST"])
def learning():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    if request.method == "GET":
        ldb.get_data(UID=uid)
        return render_template("learning.html", word=ldb.eng, defs=ldb.defs,
         path=ldb.imgurl,  maxLen=ldb.maxLen, idx=ldb.index+1)
    else:
        # answer = request.form['answer']
        # if ldb.check_answer(answer=answer):
        #     #正解
        #     return render_template("")
        # else:
        #     #不正解
        #     return render_template("")
        # ldb.submit(answer=answer)
        if not ldb.next():
            return redirect(url_for("select"))
        return render_template("learning.html", word=ldb.eng, defs=ldb.defs,
         path=ldb.imgurl, maxLen=ldb.maxLen, idx=ldb.index+1)

@app.route("/learning/answer", methods=["GET", "POST"])
def learning_answer():
    if request.method == "POST":
        answer = request.form['answer']
        ldb.submit(answer=answer)
        if ldb.isMatch:
            #正解
            return render_template("learning_answer.html",word=ldb.eng, defs=ldb.defs,
         path=ldb.imgurl, maxLen=ldb.maxLen, idx=ldb.index+1, answer=True)
        else:
            #不正解
            trueWord = ldb.imgurl.split("/")[-1].split("_")[0]
            return render_template("learning_answer.html",word=ldb.eng, defs=ldb.defs,
         path=ldb.imgurl, maxLen=ldb.maxLen, idx=ldb.index+1, answer=False, imgWord = trueWord)

@app.route("/test", methods=["GET", "POST"])
def test():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    if request.method == "GET":
        tdb.get_data(uid)
        return render_template("test.html", word=tdb.eng, defs=tdb.defs, maxLen=tdb.maxLen, idx=tdb.index+1)
    else:
        answer = request.form['answer']
        tdb.submit(answer)
        if not tdb.next():
            return redirect(url_for("select"))
        return render_template("test.html", word=tdb.eng, defs=tdb.defs, maxLen=tdb.maxLen, idx=tdb.index+1)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80,debug=True)