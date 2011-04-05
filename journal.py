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

# These views will not require password authentication
safe_views = [
    '/login', '/static/style.css', '/favicon.ico', '/static/archive.js'
]

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
        new_entry['year'] = date.year
        new_entry['month'] = date.strftime("%B %Y")
        entries.append(new_entry)
        if limit and len(entries) >= limit:
            break
    return entries

def store_entry(entry):
    """Saves entry text to a datestamped file."""
    make_entries_dir_if_not_exists()
    with open("entries/" + str(int(time.time())), "w") as f:
        f.write(entry)

@app.route('/')
def index():
    """Render the main page with up to *count* entries."""
    try:
        entries = get_entries(10)
    except (ValueError, TypeError, KeyError, OSError, IOError):
        return render_template('index.html',
            error="There was an error reading the journal.")
    else:
        return render_template("index.html", entries=entries)

@app.route('/archive')
def archive():
    """Render the archive page, with an accordion for years and months."""
    try:
        years = []
        months = {}
        entries_by_month = {}
        entries = reversed(get_entries())
        for entry in entries:
            if entry['year'] not in years:
                years.append(entry['year'])
                months[entry['year']] = []
            if entry['month'] not in months[entry['year']]:
                months[entry['year']].append(entry['month'])
                entries_by_month[entry['month']] = []
            entries_by_month[entry['month']].append(entry)
            print repr(entries_by_month)
    except (ValueError, TypeError, KeyError, OSError, IOError):
        return render_template('index.html',
            error="There was an error reading the journal.")
    else:
        return render_template("archive.html", years=years, months=months,
            entries=entries_by_month)

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
    print request.path
    if request.path in safe_views:
        return
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session.get('login_time'):
        delta = int(time.time()) - session.get('login_time')
        if delta > app.config['TIMEOUT'] and request.path != '/new':
            session['logged_in'] = None
            session['login_time'] = None
            return redirect(url_for('login'))
    session['login_time'] = int(time.time())

if __name__ == '__main__':
    app.run()
