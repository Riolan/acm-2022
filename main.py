from flask import Flask, render_template, request, redirect, session
import os
from database import QuestionTB
from random import randint
import time
import user_
import json

app = Flask(__name__, template_folder='views')
app.secret_key = 'peanut'



@app.route('/question/', methods=["POST", "GET"])

def question():
    print(session.keys())
    print()
    if 'loggedin' in session.keys():
        print(session.keys())
        if 'questions' in session.keys():
            print("ajdajkd")
            print(request)
            if request.method == "POST":
                print("POSTED")
                user_answer = request.form.get("answer")
                if user_answer == session['questions'][2]:
                    #GOT THE answ correct
                    #need to go to next question and update user with correct and time spent
                    print("correct")
                    change_data(session["loggedin"], json.dumps([session['questions'][0], (time.time()-session["time"]), (1)])  )
                    session.pop("questions", None)
                    return redirect("/question")
                else:
                    #got answ INcorrect
                    print("incorrect", session['questions'][2])
                    change_data(session["loggedin"], json.dumps([session['questions'][0], (time.time()-session["time"]), (0)])  )
                    session.pop("questions", None)
                    return redirect("/question")
            if request.method == "GET":
                print("get")
                print("starting timer")
                session["time"] = time.time()
                return render_template('index.html', question=session['questions'], username=session['loggedin'])
        else:
            print("here")
            session['questions'] = get_question()
            return render_template('index.html', question=session['questions'], username=session['loggedin'])
    
    else:
        return render_template("not_logged_in.html")


def change_data(username, data):
    print("start", user_.User.find_by_username(username))
    user_.User.update_data(username, data)
    print("end", user_.User.find_by_username(username))
    


@app.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        session['loggedin'] = username
        user_.UserRegister().post()
        print("Successfully created a user probably... i didnt do any checks so the user info entered could be completely wrong and still work")
        return redirect('/question')
    if request.method == "GET":
        return render_template('signup.html')

    
@app.route('/signin', methods=["POST","GET"])
def signin():
    if request.method == "POST":
        print("not checking to see if it works, assuming")
        username = request.form.get("username")
        password = request.form.get("password")
        user_.User().find_by_username(username)
        
        session['loggedin'] = username
        return redirect('/question')
    if request.method=="GET":
        return render_template('signin.html')

@app.route('/signout', methods=["GET", "POST"])
def signout():
    print("???")
    session.pop("loggedin", None)
    return redirect("/signin")

    
def get_question():
    print("Sizeofdb:", QuestionTB.size_of_db())
    return QuestionTB.access_data(randint(0, QuestionTB.size_of_db()))


if __name__ == '__main__':
    app.run(port=5000 ,threaded=True)
    global current_question
    #current_question = get_question()
