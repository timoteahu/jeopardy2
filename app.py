from flask import Flask, render_template, url_for, session, redirect, request
import json
import random

app = Flask('app')
app.config['SESSION_TYPE'] = 's e c r e t'
app.secret_key = 's e c r e t'




questionList = {}

# This function just generations a random category for the user and adds it to the question list which is a dictionary/map
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

# This function handles the submissions of the user and checks whether or not the answer was correct. 
# If it was, return an object of the inbetween class with a positive remark and vice versa. 

@app.route("/submitQuestion/<id>", methods=['POST', 'GET'])
def submitQuestion(id):
    newID = int(id)
    answer = request.form['answer']
    questionAnswer = session["vals"][newID]['Answer']

    if answer == questionAnswer:
        return render_template("/inbetween.html", answer = questionAnswer, text="You Got it Right!", id=newID)
    else:
        return render_template("/inbetween.html", answer = questionAnswer, text="You got it wrong!", id=newID)


#This function displays the questions page to the user with the specific question within that specific category.
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

#This function just returns the first question 
@app.route("/questions")
def firstQuestion():
    return redirect("/questions/0")

#This function returns the end page
@app.route("/endPage")
def endPage():
    return render_template("/endPage.html")

#This function retruns the in between page
@app.route("/inBetween/<id>")
def inBetween(id):
    return render_template("inbetween.html")

#This function returns the home page
@app.route("/")
def index():
    return render_template("/index.html")

#This runs the program on a server (localhost)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1000, debug=True)