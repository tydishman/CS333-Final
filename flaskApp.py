from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # handle login logic here
        return redirect(url_for("personalView"))
    return render_template("login.html")

@app.route("/signup/", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Placeholder: Add user to database here
        print(f"New user: {username}, {email}, {password}")

        return redirect(url_for("login"))  # Redirect to login after signup

    return render_template("signup.html")


@app.route("/main/")
def personalView():
    return render_template("dashboard.html")

#@app.route("/<username>/")
#def personalView(username):
    #heres where we start referencing the database for their personal events and settings \
 #   pass

if __name__ == "__main__":
    app.run(debug=True)