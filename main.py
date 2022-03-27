from flask import Flask, render_template, request
import os
from database import access_data, size_of_db
from random import randint
import time
app = Flask(__name__, template_folder='views')



@app.route('/question/<string:name>', methods=["POST", "GET"])
def question(name):
    x = time.time()
    if 'current_question' in locals():
        pass
    else:
        current_question = get_question()
    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer == current_question[2]:
            print("F")
            return render_template("index.html", question=get_question()[1])
        else:
            print("U")
            return render_template("index.html", question=current_question[1])
    if request.method == "GET":
        current_question = get_question()
        print("get")
        return render_template('index.html', question=current_question[1])

def get_question():
    
    return access_data(randint(0, size_of_db()))


if __name__ == '__main__':
    app.run(port=5000 ,threaded=True)
    global current_question
    #current_question = get_question()
