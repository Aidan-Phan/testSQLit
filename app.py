from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
# CREATED BY CHATPGT
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random secret key

# Database configuration
DATABASE = 'employees.db'

# Admin password
PASSWORD = "LUNA"

# Function to execute SQL queries
def execute_query(query, args=(), fetch=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        if fetch:
            return cursor.fetchall()
        conn.commit()

# Create the "employees" table if it doesn't exist
def init_db():
    execute_query('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT NOT NULL,
            last TEXT NOT NULL,
            pay INTEGER NOT NULL
        )
    ''')

# Route to display the table (always accessible)
@app.route('/')
def index():
    # Fetch all records from the "employees" table
    records = execute_query('SELECT * FROM employees', fetch=True)
    is_authenticated = session.get('authenticated', False)
    return render_template('website.html', records=records, is_authenticated=is_authenticated)

# Route for login
@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if password == PASSWORD:
        session['authenticated'] = True
    return redirect(url_for('index'))

# Route to handle adding an employee (requires authentication)
@app.route('/add', methods=['POST'])
def add_employee():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    # Get form data
    first = request.form['first']
    last = request.form['last']
    value = request.form['value']

    # Insert data into the database
    execute_query('INSERT INTO employees (first, last, pay) VALUES (?, ?, ?)', (first, last, value))

    return redirect(url_for('index'))

# Route to handle removing an employee (requires authentication)
@app.route('/remove', methods=['POST'])
def remove_employee():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    # Get employee ID
    emp_id = request.form['id']

    # Remove the employee from the database
    execute_query('DELETE FROM employees WHERE id = ?', (emp_id,))

    return redirect(url_for('index'))

# Route to increase pay by 1 (requires authentication)
@app.route('/increase', methods=['POST'])
def increase_pay():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    # Get employee ID
    emp_id = request.form['id']

    # Increase pay
    execute_query('UPDATE employees SET pay = pay + 1 WHERE id = ?', (emp_id,))

    return redirect(url_for('index'))

# Route to decrease pay by 1 (requires authentication)
@app.route('/decrease', methods=['POST'])
def decrease_pay():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    # Get employee ID
    emp_id = request.form['id']

    # Decrease pay
    execute_query('UPDATE employees SET pay = pay - 1 WHERE id = ?', (emp_id,))

    return redirect(url_for('index'))

# Route to logout
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the Flask app
    app.run(debug=True)
