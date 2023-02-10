from flask import Flask, render_template, url_for, session, redirect
import os
import json
import random

app = Flask('app')
app.config['SESSION_TYPE'] = 's e c r e t'
app.secret_key = 's e c r e t'

questionList = {}
@app.route("/randomCategory")
def randomCat():
    json_file = "./static/data/jeopardy.json"
    with open(json_file, 'r') as j:
        contents = json.loads(j.read())
    for content in contents:
        if(content['Category'] in questionList):
            questionList[content['Category']].append(content)
        else:
            questionList[content['Category']] = []
            questionList[content['Category']].append(content)
    vals = random.choice(list(questionList.values()))
    session.clear()
    session["vals"] = vals
    return render_template("/category.html", category= vals[0]['Category'], questions = vals)

@app.route("/questions")
def firstQuestion():
    return redirect("/questions/0")


@app.route("/questions/<id>")
def questions(id):
    newID = int(id)
    print(len(session["vals"]))
    if(newID == len(session["vals"])):
        print("equal!!!")
        return redirect("/endPage")
    if(newID >= 5):
        return redirect("/endPage")
    return render_template("/questions.html", value=session["vals"][newID], id=newID)

@app.route("/endPage")
def endPage():
    return render_template("/endPage.html")

@app.route("/inBetween/<id>")
def inBetween(id):
    return render_template("inbetween.html")

@app.route("/")
def index():
    return render_template("/index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1000, debug=True)