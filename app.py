from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3
import os
# CREATED with the help of chatgpt
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random secret key
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Database configuration
DATABASE = 'employees.db'

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not Found'}), 404
  
@app.route('/__glitch_loading_status__', methods=['GET'])
def glitch_loading_status():
    return jsonify({"status": "ok"}), 200




from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return "", 204  # Respond with no content


# Admin password
PASSWORD = "LUNA"

print("Flask app is starting...")
print("Registered routes:")
print(app.url_map)

@app.route('/cwd')
def cwd():
    import os
    return f"Current working directory: {os.getcwd()}"
  
def init_db():
    execute_query('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT NOT NULL,
            last TEXT NOT NULL,
            pay INTEGER NOT NULL
        )
    ''')
    
    
@app.route('/templates')
def templates_dir():
    
    return str(os.listdir('templates'))
  
  
# Function to execute SQL queries
def execute_query(query, args=(), fetch=False):
    print(f"Executing query: {query} with args: {args}")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        if fetch:
            result = cursor.fetchall()
            print(f"Query fetch result: {result}")
            return result
        conn.commit()
        print("Query committed successfully")

        
@app.route('/debug')
def debug():
    return "Debug route is working!"


@app.route('/templates-debug')
def templates_debug():
    import os
    try:
        return f"Templates folder contents: {os.listdir('templates')}"
    except FileNotFoundError:
        return "Templates folder not found."

# Route to display the table (always accessible)

@app.route('/')
def index():
    print("Index route called")
    records = execute_query("SELECT * FROM employees", fetch=True)
    print(f"Fetched records: {records}")
    is_authenticated = session.get('authenticated', False)
    return render_template('index.hbs', records=records, is_authenticated=is_authenticated)


# @app.route('/')
# def index():
#     print("Index route called")
#     is_authenticated = session.get('authenticated', False)
#     print(f"Authenticated: {is_authenticated}")
#     return render_template('index.html', records=[], is_authenticated=is_authenticated)



# Route for login
@app.route('/login', methods=['POST'])
def login():
    print("Login route called")  # Debugging statement
    password = request.form.get('password')
    if password == "LUNA":
        session['authenticated'] = True
        return redirect(url_for('index'))
    else:
        return "Unauthorized: Invalid Password", 403


# Route to handle adding an employee (requires authentication)
@app.route('/add', methods=['POST'])
def add_employee():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    # Debugging: Print form data
    print(f"Form data received for add_employee: {request.form}")

    # Get form data
    first = request.form.get('first')
    last = request.form.get('last')
    value = request.form.get('value')

    # Debugging: Print extracted data
    print(f"Extracted data - First: {first}, Last: {last}, Pay: {value}")

    # Insert data into the database
    execute_query('INSERT INTO employees (first, last, pay) VALUES (?, ?, ?)', (first, last, value))

    return redirect(url_for('index'))


# Route to handle removing an employee (requires authentication)
@app.route('/remove', methods=['POST'])
def remove_employee():
    if not session.get('authenticated'):
        return "Unauthorized: Login required", 403

    emp_id = request.form.get('id')
    print(f"Received request to remove employee with id: {emp_id}")

    # Debugging: Check if emp_id is valid
    if not emp_id:
        print("Error: No id provided in the form data")
        return "Bad Request: Missing ID", 400

    # Execute the query to remove the employee
    execute_query('DELETE FROM employees WHERE id = ?', (emp_id,))
    print(f"Employee with id {emp_id} removed from database")

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
  
@app.route('/debug-db')
def debug_db():
    result = execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';", fetch=True)
    if result:
        return "Employees table exists!"
    else:
        return "Employees table is missing!"

# Route to logout
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))
  
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=3000, debug=True)
