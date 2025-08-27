from flask import Flask,render_template,redirect,url_for
import pyttsx3
# import speech_recognition as sr
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start')
def start_recording():
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


# import speech_recognition as sr

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# r = sr.Recognizer()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def get_input():
#     with sr.Microphone() as source:
#         print("Talk")
#         audio_text = r.listen(source)
#         print("Time over, thanks")

#         try:
#             user_input = r.recognize_google(audio_text)
#             print("You said:", user_input)
#             return user_input.lower()
#         except sr.UnknownValueError:
#             print("Sorry, I did not get that.")
#             return None
#         except sr.RequestError:
#             print("Could not connect to Google Speech Recognition service.")
#             return None

# def generate_response(user_input):
#     greetings = ["hi", "hello"]
#     if user_input in greetings:
#         response = "Hi, I am Mat!"
#     else:
#         response = "How can I help?"
#     speak(response)
#     return response

# def main():
#     user_input = get_input()
#     if user_input:
#         response = generate_response(user_input)
#         print(response)
