from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import my_auth
import db_interface
import db

from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime, timedelta
from collections import namedtuple
import numpy as np
import graph
from calendar import monthrange
from http import HTTPStatus

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "login_error")
            return redirect(url_for('landing'))
        return view_func(*args, **kwargs)
    return wrapped_view

# Dummy database
# fake_db = {
#     "testuser": {
#         "username": "testuser",
#         "email": "test@example.com",
#         "password_hash": generate_password_hash("password123")
#     }
# }

# def get_user_by_username(username):
#     return fake_db.get(username)

# def get_user_by_email(email):
#     return fake_db.get(email)

# def get_user_by_username_or_email(identifier):
#     for user in fake_db.values():
#         if user["username"] == identifier or user["email"] == identifier:
#             return user
#     return None

# def addUser(username, email, password):
#     if username in fake_db or email in fake_db:
#         return False  # Username already exists
#     fake_db[username] = {
#         "username": username,
#         "email": email,
#         "password_hash": generate_password_hash(password)
#     }
#     return True

@app.route("/")
def landing():
    if 'user_id' in session:
        return redirect(url_for("personalView"))
    return render_template("landingPage.html")

@app.route("/signup/", methods=["POST"])
def sign_up():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("Please fill out all fields.", "signup_error")
        return redirect(url_for("landing"))

    success = my_auth.create_user(username, email, password)
    if(success):
        flash("Sign up successful. You can now log in.", "signup_success")
    else:
        flash("Sign up failed. Please try again", "signup_error")
    return redirect(url_for("landing"))

@app.route("/login/", methods=["POST"])
def login():
    identifier = request.form.get("username") or request.form.get("email")
    password = request.form.get("password")

    user = my_auth.login_user_from_form(identifier, password)

    if user:
        session['user_id'] = user['id']
        return redirect(url_for("personalView"))

    flash("Invalid username or password", "login_error")
    return redirect(url_for("landing"))

    #need user before calendar??


# Temporary structure for events
Event = namedtuple('Event', ['date', 'amount', 'description', 'type'])

@app.route("/calendar/")
@login_required
def calendar():
    user_id = session['user_id']
    month_offset = int(request.args.get('month_offset', 0))
    today = datetime.today()
    
    # Shift month by offset
    shifted_month = today.replace(day=1) + timedelta(days=month_offset * 30)
    year = shifted_month.year
    month = shifted_month.month

    first_day_of_month = datetime(year, month, 1)
    days_in_month = monthrange(year, month)[1]

    # Get all transactions
    events = db_interface.find_events(user_id)
    print(events)
    return render_template(
        "calendar.html",
        current_month=first_day_of_month.strftime("%B"),
        current_year=year,
        month_offset=month_offset,
        first_day_of_month=first_day_of_month,
        days_in_month=days_in_month,
        events=events
    )

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

@app.route('/budget/', methods=['GET', 'POST'])
@login_required
def budget():
    #user_id = current_user.id 
    #if request.method == 'POST':
    #    allocations = request.form.to_dict()
    #    for category, percent in allocations.items():
    #        # Save or update each allocation (you’ll need a Budget table)
    #        existing = Budget.query.filter_by(user_id=user_id, category=category).first()
    ##        if existing:
     #           existing.percentage = float(percent)
      #      else:
       #         db.session.add(Budget(user_id=user_id, category=category, percentage=float(percent)))
        #db.session.commit()
        #flash("Budget updated!", "success")
        #return redirect(url_for('budget'))

    #current_allocations = Budget.query.filter_by(user_id=user_id).all()
    #return render_template('budget.html', allocations=current_allocations)

    # Simulate session-based user
    dummy_user_id = 1

    # Static in-memory "database" — gets reset on app restart
    if 'dummy_budgets' not in session:
        session['dummy_budgets'] = {
            'Rent': 30.0,
            'Groceries': 20.0,
            'Savings': 15.0,
            'Utilities': 10.0,
            'Entertainment': 15.0,
            'Other': 10.0
        }

    if request.method == 'POST':
        allocations = request.form.to_dict()
        session['dummy_budgets'] = {
            k: float(v) for k, v in allocations.items()
        }
        flash("Budget updated! (dummy)", "success")
        return redirect(url_for('budget'))

    allocations = session['dummy_budgets']
    return render_template('budget.html', allocations=allocations)


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/dashboard/")
@login_required
def personalView():
    if 'user_id' not in session:
        return redirect(url_for("landing"))
    
    transaction_list = db.get_transactions_of_user(session['user_id'])

    pie_html, bar_html = graph.generate_graphs(transaction_list, None, 5000.00) 
    return render_template("dashboard.html", pie_html=pie_html, bar_html=bar_html)

@app.route("/add_event/", methods=["POST"])
@login_required
def add_event():
    if 'user_id' not in session:
        return redirect(url_for("landing"))

    name = request.form.get("name").lower()
    description = request.form.get("description").lower()
    amount = float(request.form.get("amount"))
    category = request.form.get("category").lower()
    new_category = request.form.get("newCategory").lower()

    final_category = None
    user_id = session['user_id']
    if category == "__new__" and new_category:
        success = db_interface.add_category(user_id, new_category)
        if success:
            final_category = new_category
        else:
            flash("Failed to add new category", "event_error")
    else:
        final_category = category


    # Use new category if selected
    # final_category = new_category if category == "__new__" and new_category else category

    event_type = request.form.get("type")
    expense_bool = event_type.lower() == "expense"

    date_str = request.form.get("date")
    print(date_str)
    recurring = 'recurring' in request.form

    print(f"[NEW EVENT] {name} | ${amount} | {final_category} | {event_type} | {date_str} | Recurring: {recurring}")

    success = db_interface.add_transaction(user_id, name, description, final_category, amount, recurring, expense_bool, date_str)

    if success:
        flash("Event added successfully!", "event_success")
        return redirect(url_for("personalView"))
    else:
        flash("Failed to add event", "event_error")

    # return Response(status=HTTPStatus.NO_CONTENT)
    recurrence_type = request.form.get("recurrence_type")
    custom_days = request.form.get("custom_days", "")

    original_date = datetime.strptime(date_str, "%Y-%m-%d")
    events_to_add = [Event(original_date, amount, description, event_type)]

    # Generate future recurring events
    if recurring:
        for i in range(1, 6):  # Create 6 recurrences for now
            if recurrence_type == "weekly":
                next_date = original_date + timedelta(weeks=i)
                events_to_add.append(Event(next_date, amount, description, event_type))
            elif recurrence_type == "biweekly":
                next_date = original_date + timedelta(weeks=i * 2)
                events_to_add.append(Event(next_date, amount, description, event_type))
            elif recurrence_type == "monthly":
                next_month = original_date.month + i
                year = original_date.year + (next_month - 1) // 12
                month = (next_month - 1) % 12 + 1
                try:
                    next_date = original_date.replace(year=year, month=month)
                except ValueError:
                    next_date = original_date.replace(year=year, month=month, day=28)  # Safe fallback
                events_to_add.append(Event(next_date, amount, description, event_type))
            elif recurrence_type == "custom_days":
                days = [int(d.strip()) for d in custom_days.split(",") if d.strip().isdigit()]
                for m in range(1, 4):  # Next 3 months
                    for d in days:
                        try:
                            next_date = original_date.replace(month=original_date.month + m, day=d)
                            events_to_add.append(Event(next_date, amount, description, event_type))
                        except ValueError:
                            continue

    # TODO: Save these to DB later
    for ev in events_to_add:
        print(f"[ADD EVENT] {ev.date} - {ev.amount} - {ev.description} ({ev.type})")

    flash("Event(s) added successfully!", "event_success")
    
    return redirect(url_for('personalView'))

if __name__ == "__main__":
    app.run(debug = True)