from flask import Flask,render_template,redirect,url_for
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start')
def start_recording():
    # Run in background so Flask doesn't hang
    # threading.Thread(target=listen_for_keyword_and_record).start()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
