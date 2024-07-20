from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session encryption

@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], visits=session['visits'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['visits'] = 1
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('visits', None)
    return redirect(url_for('login'))

@app.route('/increment')
def increment_visits():
    if 'visits' in session:
        session['visits'] += 1
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)