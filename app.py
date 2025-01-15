from flask import Flask, render_template, request, redirect
import sqlite3
import sqlite_demo

app = Flask(__name__)

# Database setup
DATABASE = 'employee.db'


def execute_query(query, args=(), fetch=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        if fetch:
            return cursor.fetchall()


# Routes

@app.route('/')
def home():
    return index()

def index():
    return render_template('website.html')

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/')
def index():
    # Fetch data from the database
    records = execute_query('SELECT * FROM your_table', fetch=True)
    return render_template('website.html', records=records)


@app.route('/add', methods=['POST'])
def add_record():
    # Add a new record to the database
    # name = request.form['name']
    first = request.form['first']
    last = request.form['last']
    pay = request.form['pay']
    execute_query('INSERT INTO your_table (name, value) VALUES (?, ?)', (first, last, pay))
    return redirect('/')


@app.route('/delete/<int:record_id>')
def delete_record(record_id):
    # Delete a record from the database
    execute_query('DELETE FROM your_table WHERE id = ?', (record_id,))
    return redirect('/')

