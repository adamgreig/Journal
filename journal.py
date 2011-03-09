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
app.config.from_object('config')

# These views will require password authentication
protected_views = ['/', '/all', '/new', '/logout']

def make_entries_dir_if_not_exists():
    if "entries" not in os.listdir("."):
        os.mkdir("./entries")

def get_entries(limit=None):
    """Returns a list of entries {date, body} from the entries/ folder."""
    make_entries_dir_if_not_exists()
    entries = []
    files = reversed(sorted(os.listdir("entries/")))
    for filename in files:
        with open("entries/" + filename) as f:
            body = Markup.escape((f.read())).replace("\n", Markup("<br />"))
        date = datetime.datetime.fromtimestamp(float(filename))
        new_entry = {'date': date.strftime("%H:%M, %A %d %B %Y"), 'body': body}
        entries.append(new_entry)
        if limit and len(entries) >= limit:
            break
    return entries

def store_entry(entry):
    """Saves entry text to a datestamped file."""
    make_entries_dir_if_not_exists()
    with open("entries/" + str(int(time.time())), "w") as f:
        f.write(entry)

def show_entries(count=None):
    """Render the main page with up to *count* entries."""
    try:
        entries = get_entries(count)
    except (ValueError, TypeError, KeyError, OSError, IOError):
        return render_template('index.html',
            error="There was an error reading the journal.")
    else:
        return render_template('index.html', entries=entries)

@app.route('/')
def index():
    return show_entries(10)

@app.route('/all')
def all():
    return show_entries()

@app.route('/new', methods=['POST'])
def new():
    try:
        store_entry(request.form['entry'])
    except (ValueError, TypeError, OSError, IOError):
        flash("Error adding entry.")
    else:
        flash("Entry added.")
    finally:
        return redirect(url_for("index"))

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Show a login form and check the submitted password."""
    error = None
    if request.method == 'POST':
        password = sha256(request.form['password']).hexdigest()
        if password == app.config['PASSWORD']:
            session['logged_in'] = True
            session['login_time'] = int(time.time())
            flash("Logged in successfully.")
            return redirect(url_for('index'))
        else:
            error = "Invalid password."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('login_time', None)
    flash("Logged out successfully.")
    return redirect(url_for('login'))

@app.before_request
def check_auth():
    if request.path not in protected_views:
        return
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session.get('login_time'):
        delta = int(time.time()) - session.get('login_time')
        if delta > app.config['TIMEOUT']:
            return redirect(url_for('login'))
    session['login_time'] = int(time.time())

if __name__ == '__main__':
    app.run()
