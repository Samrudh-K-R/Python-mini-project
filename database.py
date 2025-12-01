import sqlite3
import datetime

DB_NAME = 'expenses.db'

def init_db():
    """Initialize the database table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT,
            age INTEGER,
            job TEXT
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users (username)
        )
    ''')
    
    # Check if user_id column exists in expenses (migration for existing db)
    cursor.execute("PRAGMA table_info(expenses)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'user_id' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN user_id TEXT')
        
    conn.commit()
    conn.close()

# User Management Functions
def create_user(username, password, name, age, job):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, name, age, job)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, name, age, job))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_details(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, age, job FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_details(username, name, age, job):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET name = ?, age = ?, job = ? WHERE username = ?
    ''', (name, age, job, username))
    conn.commit()
    conn.close()

# Expense Functions (Updated for User Isolation)
def add_expense(date, category, amount, description, user_id):
    """Add a new expense to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, description, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, category, amount, description, user_id))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    """Retrieve all expenses ordered by date for a specific user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_expenses_by_category(user_id):
    """Retrieve total expenses grouped by category for a specific user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
