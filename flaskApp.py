from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import check_password_hash  # for comparing hashed passwords
from db import get_user_by_username  # Replace with actual DB import

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/")
def landing():
    return render_template("landingPage.html")

#make about available before signing in? or just make a lil about section in welcome page
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup/", methods=["POST"])
def signUp():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("Please fill out all fields.", "signup_error")
        return redirect(url_for("landing"))

    # TODO: Save user to DB
    print(f"New user: {username}, {email}, {password}")

    flash("Sign up successful. You can now log in.", "signup_success")
    return redirect(url_for("landing"))

@app.route("/login/", methods=["POST"])
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

    # TODO: Replace with real authentication
    if username and password:
        session['user'] = username
        return redirect(url_for("personalView"))
    else:
        flash("Invalid username or password", "login_error")
        return redirect(url_for("landing"))
    
    #need user before calendar??
@app.route("/calendar/")
def calendar():
    return render_template("calendar.html")

@app.route("/tips/")
def tips():
    return render_template("tips.html")

@app.route("/wishlist/")
def wishlist():
    return render_template("wishlist.html")

@app.route("/budget/")
def budget():
    return render_template("budget.html")

@app.route("/logout/")
def logout():
    # session.clear()  # Uncomment if using session-based auth
    return redirect(url_for("landing"))

@app.route("/main/")
def personalView():
    if 'user' not in session:
        return redirect(url_for("landing"))
    return render_template("dashboard.html")

#@app.route("/<username>/")
#def personalView(username):
    #heres where we start referencing the database for their personal events and settings \
 #   pass

if __name__ == "__main__":
    app.run(debug=True)