from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime, timedelta
from collections import namedtuple

# Temporary structure for events
Event = namedtuple('Event', ['date', 'amount', 'description', 'type'])

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
def landing():
    if 'user' in session:
        return redirect(url_for("personalView"))
    return render_template("landingPage.html")


#make about available before signing in? or just make a lil about section in welcome page
@app.route("/about")
@login_required
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
    addUser(username, email, password)
    flash("Sign up successful. You can now log in.", "signup_success")
    return redirect(url_for("landing"))

@app.route("/login/", methods=["POST"])
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
    month_offset = int(request.args.get('month_offset', 0))
    today = datetime.today()
    current_month_date = today.replace(day=1) + timedelta(days=month_offset * 30)

    # Fake data for now
    events = [
        Event(current_month_date.replace(day=5), 1200, "Freelance Project", "income"),
        Event(current_month_date.replace(day=12), 250, "Groceries", "expense"),
        Event(current_month_date.replace(day=18), 75, "Electric Bill", "expense"),
        Event(current_month_date.replace(day=22), 2000, "Paycheck", "income"),
    ]

    return render_template("calendar.html", 
                           current_month=current_month_date.strftime("%B"),
                           current_year=current_month_date.year,
                           month_offset=month_offset,
                           events=events)


@app.route("/tips/")
@login_required
def tips():
    return render_template("tips.html")

wishlist_items = []  # in-memory list for now

@app.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html', items=wishlist_items)

@app.route('/add-wishlist-item/', methods=['POST'])
@login_required
def add_wishlist_item():
    name = request.form.get('item_name')
    price = request.form.get('item_price')
    if name and price:
        wishlist_items.append({'name': name, 'price': price})
    return redirect(url_for('wishlist'))

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

@app.route("/add_event/", methods=["POST"])
@login_required
def add_event():
    if 'user' not in session:
        return redirect(url_for("landing"))

    name = request.form.get("name")
    amount = float(request.form.get("amount"))
    category = request.form.get("category")
    new_category = request.form.get("new_category")

    # Use new category if selected
    final_category = new_category if category == "__new__" and new_category else category

    event_type = request.form.get("type")
    date_str = request.form.get("date")
    recurring = 'recurring' in request.form

    print(f"[NEW EVENT] {name} | ${amount} | {final_category} | {event_type} | {date_str} | Recurring: {recurring}")

    # TODO: Save to DB

    flash("Event added successfully!", "event_success")
    return redirect(url_for("personalView"))

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
