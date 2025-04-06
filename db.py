import sqlite3


DATABASE_PATH = "database.db"


def init_tables():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()

    create_users_table = """CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT (DATETIME('now')),
        last_login TEXT,
        budget FLOAT NOT NULL DEFAULT 0.0
    );"""

    create_transactions_table = """CREATE TABLE IF NOT EXISTS transactions (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing transaction ID
        title TEXT NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,          -- Foreign key to `categories` table
        amount REAL NOT NULL,                  -- Transaction amount (can be positive or negative)
        recurring BOOLEAN DEFAULT 0,           -- Whether the transaction is recurring (1 = True, 0 = False)
        created_at TEXT DEFAULT (DATETIME('now')), -- Date and time of the transaction
        user_id INTEGER NOT NULL,              -- Foreign key to `users` table
        expense BOOLEAN NOT NULL,                 -- Transaction type (0 = Expense, 1 = Income)
        FOREIGN KEY(category_id) REFERENCES categories(ID), -- Ensures a valid category reference
        FOREIGN KEY(user_id) REFERENCES users(ID) -- Ensures a valid user reference
    );"""

    create_categories_table = """CREATE TABLE IF NOT EXISTS categories (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing category ID
        name TEXT NOT NULL UNIQUE,                    -- Category name (e.g., "Groceries", "Salary")
        user_id INTEGER NOT NULL,              -- Foreign key to `users` table
        FOREIGN KEY(user_id) REFERENCES users(ID) -- Ensures a valid user reference
    );"""

    cur.execute(create_users_table)
    cur.execute(create_transactions_table)
    cur.execute(create_categories_table)
    con.close()


def add_budget_column():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check the columns in the 'users' table
    cursor.execute("PRAGMA table_info(users);")
    columns = [column['name'] for column in cursor.fetchall()]

    # If the 'budget' column doesn't exist, add it
    if 'budget' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN budget FLOAT NOT NULL DEFAULT 0.0;")
        conn.commit()

    conn.close()

def init_test_data():
    create_user('user', 'user@email.com', 'myhash')
    user1 = get_user('user')

    create_category(user1, "Food")
    create_category(user1, "Entertainment")

    create_transaction(user1, 'McDonalds', 'minecraft meal', 1, 12.12, False, True)
    create_transaction(user1, 'Bluey plushie', 'i really want it', 2, 19.99, True, False)
    

    create_user('user2', 'user2@email.com', 'secondlyhashedpassword')
    user2 = get_user('user2')
    create_transaction(user2, 'waltuh', 'help me', 1, 123.45, False, False)

    create_user('user3', 'user3@email.com', 'hash3')
    user3 = get_user('user3')


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)  # Connect to SQLite database file
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

def print_schema():
    new_con = sqlite3.connect(DATABASE_PATH)
    new_cur = new_con.cursor()

    print(new_cur.execute("SELECT * FROM users").fetchall())
    return

    res = new_cur.execute("PRAGMA table_info([users]);")
    print(res.fetchall())
    print('-'*100)

    res = new_cur.execute("PRAGMA table_info([transactions]);")
    print(res.fetchall())
    print('-'*100)

    res = new_cur.execute("PRAGMA table_info([categories]);")
    print(res.fetchall())
    print('-'*100)

    new_con.close()

def create_user(username: str, email: str, hashed_password: str):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        user_id = cur.lastrowid  # Get the ID of the newly inserted user

        # Optional: Fetch and return full user
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()

        return dict(user) if user else None

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")  # Email or username probably already exists
        return None

    finally:
        conn.close()


def get_user(identifier:str):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ? OR ID = ?', (identifier,identifier,identifier)).fetchone()
    conn.close()
    return user

def create_transaction(user_id, title:str, description:str, category_id:int, amount:float, recurring:bool, expense:bool, input_date):
    title = title.lower()
    conn = get_db_connection()
    conn.execute("INSERT INTO transactions(title, description, category_id, amount, recurring, user_id, expense, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, description, category_id, amount, recurring, user_id, expense, input_date))
    conn.commit()
    conn.close()

def create_category(user_id, category_name:str):
    category_name = category_name.lower()
    conn = get_db_connection()
    conn.execute("INSERT INTO categories(name, user_id) VALUES (?, ?)", (category_name, user_id))
    conn.commit()
    conn.close()
    return True

# Given a user, returns all transactions of a user
def get_transactions_of_user(user_id):
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions t JOIN users u ON t.user_id = u.id WHERE u.id = ?", (user_id,))
    # conn.close()
    return transactions.fetchall()

def get_categories_of_user(user_id):
    conn = get_db_connection()
    categories = conn.execute("SELECT * FROM categories c JOIN users u ON c.user_id = u.id WHERE u.id = ?", (user_id,))
    # conn.close()
    return categories.fetchall()

def get_category_id_by_name(user_id, category_name:str):
    conn = get_db_connection()
    category_id = conn.execute("SELECT c.id FROM categories c JOIN users u ON c.user_id = u.id WHERE u.id = ? AND c.name = ?", (user_id, category_name)).fetchone()
    conn.close()
    return category_id['id']

def get_category_name_by_id(user_id, category_id:str):
    conn = get_db_connection()
    category = conn.execute("SELECT c.name FROM categories c JOIN users u ON c.user_id = u.id WHERE u.id = ? AND c.id = ?", (user_id, category_id)).fetchone()
    conn.close()
    return category['name']

def save_user_budget(user_id, total_budget):
    conn = get_db_connection()

    # Update the user's budget
    conn.execute("UPDATE users SET budget = ? WHERE ID = ?", (total_budget, user_id))
    conn.commit()
    conn.close()

def get_user_budget(user_id):
    conn = get_db_connection()
    budget_query = "SELECT budget FROM users WHERE ID = ?"
    budget_result = conn.execute(budget_query, (user_id,)).fetchone()
    total_budget = budget_result[0] if budget_result else 0.0

    conn.close()

    return total_budget

if __name__ == "__main__":
    init_tables()
    # init_test_data()