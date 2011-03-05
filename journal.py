# Journal
# A simple journal web application.
# Adam Greig, 2011. All code released into the public domain.

import os
import time
import datetime
from hashlib import sha256
from flask import Flask, Markup
from flask import request, session, redirect, url_for, render_template, flash

app = Flask(__name__)
app.config.from_object('password')
app.config.from_object('config')

def make_entries_dir_if_not_exists():
    """Makes the entries/ directory if it doesn't exist."""
    if "entries" not in os.listdir("."):
        os.mkdir("./entries")

def get_entries():
    """Returns a list of entry dicts from the entriess/ folder."""
    make_entries_dir_if_not_exists()
    entries = []
    files = reversed(sorted(os.listdir("entries/")))
    for filename in files:
        with open("entries/" + filename) as f:
            body = Markup.escape((f.read())).replace("\n", Markup("<br />"))
        date = datetime.datetime.fromtimestamp(float(filename))
        new_entry = {'date': date.strftime("%H:%M, %A %d %B %Y"), 'body': body}
        entries.append(new_entry)
    return entries

def store_entry(entry):
    """Saves entry text to a datestamped file."""
    make_entries_dir_if_not_exists()
    with open("entries/" + str(int(time.time())), "w") as f:
        f.write(entry)

@app.route('/')
def index():
    """List the most recent entries, with a text box for a new entry."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        entries = get_entries()[:10]
    except (ValueError, TypeError, KeyError, OSError, IOError):
        entries = []
    return render_template('index.html', entries=entries)

@app.route('/all')
def all():
    """View all entries."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        entries = get_entries()
    except (ValueError, TypeError, KeyError, OSError, IOError):
        entries = []
    return render_template('index.html', entries=entries)

@app.route('/new', methods=['POST'])
def new():
    """Stores a new entry."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    store_entry(request.form['entry'])
    flash("Entry added.")
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

if __name__ == '__main__':
    app.run()
