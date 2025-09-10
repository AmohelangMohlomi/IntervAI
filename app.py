from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Login page route (starting page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Dummy authentication, replace with your logic
        if username == 'user' and password == 'pass':
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.', 'error')

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    render_template("signup.html")



if __name__ == '__main__':
    app.run(debug=True)
