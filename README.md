# IntervAI

IntervAI is an interactive interview preparation app that helps users practice answering common interview questions. It fetches questions from a SQLite database (questions.db), then displays them one by one. Users can respond via voice input or text input, and the app provides real-time feedback and tips to help improve their answers.

## Demo

### You can have a look of a live demo of IntervAI here:
[![Watch the video](https://img.youtube.com/vi/d9qay6OnMig/0.jpg)](https://www.youtube.com/watch?v=d9qay6OnMig)



### Note: Users must log in to use the app so that their interview progress and responses can be saved securely.

## Features

- User authentication and login system

- Interview questions fetched from a local SQLite database

- Supports both voice and text input for user responses

- Provides AI-generated feedback and tips on answers using the SheCodes AI API

- Saves user interview sessions and responses for progress tracking

- User-friendly interface built with HTML, CSS, and JavaScript

- Powered by Flask backend and Python for server-side logic

## Tech Stack

- Backend: Flask, Python

- Frontend: JavaScript, HTML, CSS

- Database: SQLite (questions.db) for questions and user data, (users.db) for the list of users and their saved interviews.

- AI API: SheCodes AI API

## Getting Started
### Prerequisites

- Python 3.x

- Flask

- SQLite3

- Access to SheCodes AI API

## Installation

### Clone the repo:

- git clone https://github.com/AmohelangMohlomi/IntervAI.git
- cd intervai 


### Install dependencies:

- pip install -r requirements.txt 


### Set up your environment variables for SheCodes AI API and any secret keys (for example, Flask secret key for sessions).

- Run the Flask app:

- flask run
- Open your browser and go to http://localhost:5000

- Create an account or log in to start practicing interviews.

## How It Works

1. Users create an account and log in to the app.

2. The app loads an interview question from the SQLite database.

3. The question is displayed on the web interface.

4. Users answer by speaking or typing their response.

5. The answer is sent to the backend and analyzed by the SheCodes AI API.

6. Feedback and tips are provided to the user.

7. User responses and progress are saved in the database tied to their account.


## Future Improvements

- Enhance user profile and progress dashboards

- Add password reset and email verification and logging in with google

- Support multiple languages for both questions and feedback

- Add interview scheduling and reminders

- Improve voice recognition accuracy

## License

This project is licensed under the MIT License - see the LICENSE file for details.