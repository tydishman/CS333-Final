from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.", "login_error")
            return redirect(url_for('landing'))
        return view_func(*args, **kwargs)
    return wrapped_view

# Dummy database
fake_db = {
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": generate_password_hash("password123")
    }
}

def get_user_by_username(username):
    return fake_db.get(username)

def get_user_by_email(email):
    return fake_db.get(email)

def get_user_by_username_or_email(identifier):
    for user in fake_db.values():
        if user["username"] == identifier or user["email"] == identifier:
            return user
    return None

def addUser(username, email, password):
    if username in fake_db or email in fake_db:
        return False  # Username already exists
    fake_db[username] = {
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password)
    }
    return True

@app.route("/")
@login_required
def landing():
    return render_template("landingPage.html")

#make about available before signing in? or just make a lil about section in welcome page
@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/signup/", methods=["POST"])
@login_required
def signUp():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("Please fill out all fields.", "signup_error")
        return redirect(url_for("landing"))

    # TODO: Save user to DB
    fake_db.addUser(username, email, password)
    flash("Sign up successful. You can now log in.", "signup_success")
    return redirect(url_for("landing"))

@app.route("/login/", methods=["POST"])
@login_required
def login():
    identifier = request.form.get("username") or request.form.get("email")
    password = request.form.get("password")

    user = get_user_by_username_or_email(identifier)

    if user and check_password_hash(user["password_hash"], password):
        session['user'] = user['username']
        return redirect(url_for("personalView"))

    flash("Invalid username or password", "login_error")
    return redirect(url_for("landing"))

    #need user before calendar??
@app.route("/calendar/")
@login_required
def calendar():
    return render_template("calendar.html")

@app.route("/tips/")
@login_required
def tips():
    return render_template("tips.html")

@app.route("/wishlist/")
@login_required
def wishlist():
    return render_template("wishlist.html")

@app.route("/budget/")
@login_required
def budget():
    return render_template("budget.html")

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/dashboard/")
@login_required
def personalView():
    if 'user' not in session:
        return redirect(url_for("landing"))
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)