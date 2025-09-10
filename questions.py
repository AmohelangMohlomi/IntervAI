import sqlite3

# Path to your database file
conn = sqlite3.connect('questions.db')  # Update path as needed
cursor = conn.cursor()

# === Make sure your table exists ===
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,          -- e.g. 'technical' or 'cultural'
        question TEXT NOT NULL
    )
''')

# === Sample questions to insert ===
questions = [
    ("technical", "Share about a project you’ve worked on at WTC and enjoyed - what did you enjoy about it, how you went about solving the problem - what approach did you take?"),
    ("technical", "Which project/s was difficult for you? Can you elaborate what about the project was difficult and how you solved it in the end?"),
    ("technical", "What kind of technical questions/ problems do you enjoy working on and why?"),
    ("technical","Which key technical concepts have you learnt on your journey at WTC and how do they fit into the broader process of developing software?"),
    ("technical","What is TDD and why is it used/ important in software development? - Can you share a practical case/ example for TDD?"),
    ("technical", "Explain concept X, Y Z to me to in detail - why is it useful / important?"),
    ("technical", "What is your methodology for solving problems?"),
    ("technical","What type of challenges have you faced with projects in your curriculum?"),
    ("cultural", "Describe a time you resolved a conflict in a team."),
    ("cultural", "How do you handle feedback from coworkers?"),
    ("cultural"," What are your aspirations in tech? What would be your ideal job/ company?")
]

# === Insert questions ===
cursor.executemany("INSERT INTO questions (category, question) VALUES (?, ?)", questions)

conn.commit()
conn.close()

print("Questions added successfully.")
