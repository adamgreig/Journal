# Journal
# A simple journal web application.
# Adam Greig, 2011. All code released into the public domain.

from flask import Flask
from flask import request, session, redirect, url_for, render_template, flash

from hashlib import sha256

app = Flask(__name__)
app.config.from_object('password')
app.config.from_object('config')

@app.route('/')
def index():
    """List the most recent posts, with a text box for a new post."""
    posts = [
        {'date': '4th March 2011', 'body': 'this is a test'}
    ]
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    """Stores a new post."""
    flash("Post added.")
    return redirect(url_for("index"))

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Show a login form and check the submitted password."""
    error = None
    if request.method == 'POST':
        password = sha256(request.form['password']).hexdigest()
        if password == app.config['PASSWORD']:
            session['logged_in'] = True
            flash("Logged in successfully.")
            return redirect(url_for('index'))
        else:
            error = "Invalid password."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Log the user out."""
    session.pop('logged_in', None)
    flash("Logged out successfully.")
    return redirect(url_for('login'))

@app.before_request
def before_request():
    """
    Before any request, check that the user is logged in. If they are not,
    redirect them to the login page instead.
    Special exception: don't stop them from logging in.
    """
    if not session.get('logged_in') and request.path != "/login":
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
