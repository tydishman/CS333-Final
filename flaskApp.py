from flask import Flask, redirect, url_for, render_template 

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>wassup</h1>"

@app.route("/login/", methods = ["POST", 'GET'])
def login():
    pass

if __name__ == "__main__":
    app.run(debug = True)