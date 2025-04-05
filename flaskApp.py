from flask import Flask, render_template, request, redirect, url_for, session, flash

from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime, timedelta
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

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

    # Define spending categories and values
    categories = ["Housing", "Food", "Entertainment"]
    subcategories = [["Rent", "Utilities"], ["Groceries", "Dining Out"], ["Movies", "Games"]]
    vals = np.array([[50., 340], [40., 50.], [45., 70.]])  # Sub-category spending

    # Define total budget
    total_budget = 4000  # Example total monthly budget
    total_spent = vals.sum()  # Sum of all spending
    remaining = total_budget - total_spent  # Money left or over budget

    # Function to create a gradient of pastel shades
    def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
        alphas = np.linspace(alpha_start, alpha_end, n)  # Smooth gradient
        shades = []
        for i, alpha in enumerate(alphas):
            darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
            shades.append([(1 - alpha) + alpha * c for c in darkened_color])
        return shades

    # Define number of categories
    num_main_categories = 3  
    num_subcategories = 6  

    # Define base colors
    base_color_outer = (0.87, 0.73, 0.66)  # Pastel brown (#debaa9) - starts light
    base_color_inner = (0.74, 0.86, 0.81)  # Deep pastel green

    # Generate gradients
    outer_colors = pastel_gradient(num_main_categories, base_color_outer, alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)  # Darker brown shades
    inner_colors = pastel_gradient(num_subcategories, base_color_inner, alpha_start=0.6, alpha_end=0.95)  # Green gradient

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns (Pie + Bar Chart)
    size = 0.3  # Thickness of the rings

    # --------- PLOT PIE CHART ---------
    outer_wedges, outer_texts, _ = axes[0].pie(vals.sum(axis=1), radius=1, labels=categories, 
                                               autopct='%1.1f%%', pctdistance=0.9,  
                                               labeldistance=1.1,  
                                               colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))

    inner_wedges, inner_texts, _ = axes[0].pie(vals.flatten(), radius=1-size, labels=np.concatenate(subcategories), 
                                               autopct='%1.1f%%', pctdistance=0.85,  
                                               labeldistance=1.2,  
                                               colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))

    axes[0].set(aspect="equal", title="Spending Breakdown (Pastel Brown & Green Gradient)")

    # --------- PLOT BAR CHART ---------
    labels = ["Budget", "Spent", "Remaining"]
    values = [total_budget, total_spent, remaining]

    bars = axes[1].bar(labels, values, color=["#debaa9", "#f6f0e4", "#bddbcf"])  # Using pastel brown for bars

    for bar in bars:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, yval + 50, f"${yval}", ha='center', fontsize=12)

    axes[1].set_ylabel("Amount ($)")
    axes[1].set_title("Budget vs. Actual Spending")

    plt.tight_layout()
    plt.savefig('static/graphs.png')  # Save the figure

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
    app.run(debug=True)