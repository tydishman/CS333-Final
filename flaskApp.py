from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # handle login logic here
        return redirect(url_for(""))
    return render_template("login.html")

@app.route("/<username>")
def personalView(username):
    #heres where we start referencing the database for their personal events and settings \
    pass

if __name__ == "__main__":
    app.run(debug=True)