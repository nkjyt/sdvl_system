from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pyrebase
import json, os, re
import database.database as database
import database.timer as f_timer
import deepl

with open("firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = os.urandom(24)

mdb = database.memorizeDB()
adb = database.associationDB()
jdb = database.japaneseDB()
# fdb = database.feedbackDB()
# fadb = database.feedback_associationDB()
andb = database.annotationDB()
ldb = database.learningDB()
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

@app.route("/memorize", methods=['GET', 'POST'])
def memorize():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        w = mdb.getUserWords(ini.uid)
        timer.start_timer()
        if w == '':
            mdb.reset()
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
            timer.record_time()
            if query == "remembered":
                mdb.remembered()
            else:
                mdb.notRemembered()
            if mdb.nextWord():
                w = mdb.eng
            else:
                return redirect(url_for("select"))

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
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))

    data = {
        "eng" : "",
        "jpn" : "",
        "pos" : "",
        "hint" : "",
        "keywords" : [],
    }
    if request.method == 'GET':
        w = adb.getUserWords(ini.uid)
        timer.start_timer()
        if w == '':
            adb.reset()
            return redirect(url_for('select'))
        else:
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [rep(word, adb.eng) for word in adb.imgName]
        return render_template("association.html", word = w, path=adb.imgurl, data = data)
    else:
        # adb.submit(request.form['answer'])
        timer.record_time()
        if adb.nextWord():
            data['eng'] = adb.eng
            data['jpn'] = adb.jpn
            data['pos'] = adb.pos
            data['hint'] = adb.eng[0] + "*"*(len(adb.eng)-1)
            data["keywords"] = [rep(word, adb.eng) for word in adb.imgName]
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
    data['pos'] = adb.pos
    data['answer'] = request.form['answer']
    data["keywords"] = [rep(word, adb.eng) for word in adb.imgName]
    return render_template("association_answer.html",path=adb.imgurl, data = data, msg = msg)

def rep(st, word):
    st = st.replace("_", "")
    st = st.replace(word, "")
    return st

@app.route("/japanese", methods=['GET', 'POST'])
def japanese():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    if request.method == 'GET':
        w = jdb.getUserWords(ini.uid)
        timer.start_timer()
        if w == '':
            jdb.reset()
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
            timer.record_time()
            if query == "remembered":
                jdb.remembered()
            else:
                jdb.notRemembered()
            if jdb.nextWord():
                w = jdb.eng
            else:
                return redirect(url_for("select"))

        # path = f'static/assets/{jdb.UID}/{jdb.eng}'
        return render_template("japanese.html", word = w)

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
    translator = deepl.Translator("2c1055ac-4792-7f39-4a6d-e4a77e5763ec")
    result = translator.translate_text("\n".join(andb.defs), target_lang="JA")
    res = str(result).split("\n")
    print(result)
    print(type(res))

    return render_template("annotation.html", word=andb.eng, defs=andb.defs, path=andb.imgurl,
     isTrans=True, jpn=res,  maxLen=andb.maxLen, idx=andb.index+1)

@app.route("/select/wordset", methods=["GET", "POST"])
def select_wordset():
    try:
        uid = ini.uid
    except:
        return redirect(url_for('login'))
    li = andb.get_wordlist(uid)
    return render_template("select_wordset.html", index_list=li)

@app.route("/learning", methods=["GET", "POST"])
def learning():
    try:
        uid = "OTattFQ8vHf1iuPZv94sE3Gj3G22"
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


# @app.route("/feedback", methods=["GET", "POST"])
# def feedback():
#     data = {}
#     try:
#         uid = ini.uid
#     except:
#         return redirect(url_for('login'))
#     if request.method == "GET":
#         w = fdb.get_data(ini.uid)
#         if w == '':
#             return redirect(url_for('select'))
        
#         data['eng'] = fdb.eng
#         data['jpn'] = fdb.jpn

#         return render_template("feedback.html", path=fdb.imgurl, data=data)
    
#     else:
#         fb = []
#         for i in range(9):
#             k = "img" + str(i)
#             fb.append({
#                 "url" : fdb.imgurl[i],
#                 "feedback" : request.form[k]})
#         fdb.submit(fb, fdb.eng)
#         fdb.next()
#         if not fdb.next():
#                 return redirect(url_for("select"))
            
#         data['eng'] = fdb.eng
#         data['jpn'] = fdb.jpn
#         return render_template("feedback.html", path=fdb.imgurl, data=data)


# @app.route("/feedback_association", methods=["GET", "POST"])
# def feedback_association():
#     data = {}
#     try:
#         uid = ini.uid
#     except:
#         return redirect(url_for('login'))
#     if request.method == "GET":
#         w = fadb.get_data(ini.uid)
#         if w == '':
#             return redirect(url_for('select'))
        
#         data['eng'] = fadb.eng
#         data['jpn'] = fadb.jpn
#         data['keywords'] = fadb.imgName
#         data['length'] = len(fadb.imgName)
#         return render_template("feedback_association.html", path=fadb.imgurl, data=data)
    
#     else:
#         fb = []
#         for i in range(len(fadb.imgurl)):
#             k = "img" + str(i)
#             fb.append({
#                 "url" : fadb.imgurl[i],
#                 "feedback" : request.form[k]})
#         fadb.submit(fb, fadb.eng)
#         fadb.next()
#         if not fadb.next():
#                 return redirect(url_for("select"))
            
#         data['eng'] = fadb.eng
#         data['jpn'] = fadb.jpn
#         data['keywords'] = fadb.imgName
#         data['length'] = len(fadb.imgName)
#         return render_template("feedback_association.html", path=fadb.imgurl, data=data)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80,debug=True)