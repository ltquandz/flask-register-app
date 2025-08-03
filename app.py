from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT,
        course TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        course = request.form['course']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO registrations (name, student_id, course) VALUES (?, ?, ?)",
                  (name, student_id, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM registrations")
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', data=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
