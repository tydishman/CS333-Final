from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash  # for comparing hashed passwords
from db import get_user_by_username  # Replace with actual DB import


app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>wassup</h1>"

@app.route("/login/", methods = ["POST", 'GET'])
def login():
    if request.method == "POST":
        # handle login logic here
        username = request.form['username']
        password = request.form['password']
        
        # Fetch user from database by username
        user = get_user_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):  # Password matching
            # User found and password is correct, redirect to the dashboard
            return redirect(url_for('dashboard'))  # Redirect to 'dashboard' route or user profile
            
        else:
            # Invalid credentials, show flash message
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))  # Stay on the login page
        return redirect(url_for(""))
    return render_template("login.html")

# @app.route("/<username>")
# def personalView(username):
#     #heres where we start referencing the database for their personal events and settings \
#     pass

if __name__ == "__main__":
<<<<<<< Updated upstream
    app.run(debug = True)
=======
    app.run(debug=True)



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to something secure for production

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup/", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # TODO: Add user to database here
        print(f"New user: {username}, {email}, {password}")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # TODO: Validate user login
        # This is a placeholder example:
        if username and password:
            session['user'] = username
            return redirect(url_for("personalView"))
        else:
            return "Invalid login", 401

    return render_template("login.html")

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/main/")
def personalView():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/calendar/")
def calendar():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("calendar.html")

@app.route("/tips/")
def tips():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("tips.html")

@app.route("/wishlist/")
def wishlist():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("wishlist.html")

@app.route("/budget/")
def budget():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("budget.html")

if __name__ == "__main__":
    app.run(debug=True)
'''
>>>>>>> Stashed changes
