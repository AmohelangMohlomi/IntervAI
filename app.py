from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from dotenv import load_dotenv
import os
import sqlite3
import random
import requests

load_dotenv() 

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
            session['username'] = username  
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

         # Create interviews table to store question, answer, feedback, timestamp
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                feedback TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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



def build_prompt(question, answer):
    context = f"""
    You are an interview AI called IntervAI. The question comes from a local interview question database. 
    After hearing the user's answer, you provide **detailed and constructive feedback** based on how well the answer fits a professional interview.
    Question: {question}
    User's Answer: {answer}
    """
    return context

@app.route('/get_feedback', methods=['POST'])
def get_feedback():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        return jsonify({'error': 'Missing question or answer'}), 400

    category = "cultural"  

    prompt = f"Provide interview feedback for the answer to this question and give tips to answer the question better: {question}"
    context = build_prompt(question, answer)

    api_url = "https://api.shecodes.io/ai/v1/generate"
    api_key = os.getenv("SHECODES_API_KEY")

    try:
        response = requests.get(api_url, params={
            'prompt': prompt,
            'context': context,
            'key': api_key
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            feedback = data.get("answer", "No feedback received.")
        else:
            feedback = "Error getting feedback from AI. Please try again later."

    except Exception as e:
        feedback = f"An error occurred: {str(e)}"

    username = session.get('username', 'anonymous')
    save_interview(username, category, question, answer, feedback)

    session['feedback_data'] = {
        'question': question,
        'answer': answer,
        'feedback': feedback
    }

    return jsonify({'redirect_url': url_for('show_feedback')})

@app.route('/show_feedback')
def show_feedback():
    feedback_data = session.get('feedback_data')
    if not feedback_data:
        flash("No feedback available.", "error")
        return redirect(url_for('home'))
    return render_template('feedback.html', **feedback_data)

def save_interview(username, category, question, answer, feedback):
    db = get_db()
    db.execute('''
        INSERT INTO interviews (username, category, question, answer, feedback)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, category, question, answer, feedback))
    db.commit()

@app.route('/show_history')
def show_history():
    username = session.get('username')
    if not username:
        flash("You must be logged in to view your interview history.", "error")
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.execute('''
        SELECT category, question, answer, feedback, timestamp
        FROM interviews
        WHERE username = ?
        ORDER BY timestamp DESC
    ''', (username,))
    interviews = cursor.fetchall()

    return render_template("show_history.html", interviews=interviews)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
