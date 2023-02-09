from flask import Flask, render_template, url_for, session, redirect
import os

app = Flask('app')

@app.route("/")
def index():
    return render_template("/index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1000, debug=True)