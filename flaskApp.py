from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash  # for comparing hashed passwords
from db import get_user_by_username  # Replace with actual DB import


app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/login/", methods=["GET", "POST"])
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
    app.run(debug=True)