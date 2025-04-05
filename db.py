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
        last_login TEXT
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
        type BOOLEAN NOT NULL,                 -- Transaction type (0 = Expense, 1 = Income)
        FOREIGN KEY(category_id) REFERENCES categories(ID), -- Ensures a valid category reference
        FOREIGN KEY(user_id) REFERENCES users(ID) -- Ensures a valid user reference
    );"""

    create_categories_table = """CREATE TABLE IF NOT EXISTS categories (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing category ID
        name TEXT NOT NULL,                    -- Category name (e.g., "Groceries", "Salary")
        user_id INTEGER NOT NULL,              -- Foreign key to `users` table
        FOREIGN KEY(user_id) REFERENCES users(ID) -- Ensures a valid user reference
    );"""

    cur.execute(create_users_table)
    cur.execute(create_transactions_table)
    cur.execute(create_categories_table)
    con.close()

def init_test_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users(username, email, password_hash) VALUES('test','test@email.com','myhash')")    

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)  # Connect to SQLite database file
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# def get_user_by_username(username:str):
#     conn = get_db_connection()
#     user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
#     conn.close()
#     return user

# def get_user_by_email(email:str):
#     conn = get_db_connection()
#     user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
#     conn.close()
#     return user

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

# Attempts to add user to database. Throws errors if stuff happens
def create_user(username:str, email:str, hashed_password:str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()

    res = cur.execute("INSERT INTO users (username, email, password_hash) VALUES(?,?,?)", (username,email,hashed_password))    

    # sqlite3.IntegrityError: UNIQUE constraint failed: users.email

    conn.commit()
    conn.close()

def get_user(identifier:str):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (identifier,identifier)).fetchone()
    conn.close()
    return user['password_hash']

if __name__ == "__main__":
    # init_tables()
    # init_test_data()
    # create_user("walter", "walter@email.com", "w-8t3h")
    # user = get_user("walter")
    user = get_user("walter@email.com")
    print(user)
    # print_schema()
   