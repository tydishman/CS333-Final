import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()


create_users_table = """CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);"""

create_transactions_table = """CREATE TABLE IF NOT EXISTS transactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing transaction ID
    category_id INTEGER NOT NULL,          -- Foreign key to `categories` table
    amount REAL NOT NULL,                  -- Transaction amount (can be positive or negative)
    recurring BOOLEAN DEFAULT 0,           -- Whether the transaction is recurring (1 = True, 0 = False)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date and time of the transaction
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

new_con = sqlite3.connect("tutorial.db")
new_cur = new_con.cursor()
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