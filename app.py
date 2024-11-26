from flask import Flask, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# TODO import config from config file
app.config['SQKALCHEMY_DATABSE_URI'] = 'yawgbargain-db.c5uok8ai4zek.us-east-1.rds.amazonaws.com'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    session['user'] = {'name': 'Joshua Carson', 'email': 'joshua@example.com'}
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/decks')
def decks():
    return 'My Decks Page'

@app.route('/profile')
def profile():
    return 'My Profile Page'

if __name__ == '__main__':
    # SEE FLASK
    # SEE FLASK RUN
    # RUN FLASK RUN
    app.run(debug=True,host='0.0.0.0',port=8080)

