from flask import Flask, render_template, session, redirect


app = Flask(__name__)


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
    app.run(debug=True,port=80,host='0.0.0.0')

