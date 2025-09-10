from flask import Flask, render_template, request, redirect, url_for, flash,g
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

DATABASE = 'users.db' 


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)
        if user and user['password'] == password:  
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.', 'error')

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('signup.html')

        # Try to add user to DB
        success = add_user(username, password)  # You might want to hash the password here!

        if success:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')

    return render_template('signup.html')


# Connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close DB when app context ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize DB and create user table
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

# User lookup function
def get_user(username):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone()

# Add a new user (for testing or signup)
def add_user(username, password):
    try:
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_random_question(category):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question FROM questions WHERE category = ?", (category,))
    questions = cursor.fetchall()
    conn.close()

    if questions:
        return random.choice(questions)[0]
    else:
        return "No questions available in this category."

@app.route('/technical')
def technical():
    question = get_random_question("technical")
    return render_template("technical.html", question=question)

@app.route('/cultural')
def cultural():
    question = get_random_question("cultural")
    return render_template("cultural.html", question=question)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
