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

def make_posts_dir_if_not_exists():
    """Makes the posts/ directory if it doesn't exist."""
    if "posts" not in os.listdir("."):
        os.mkdir("./posts")

def get_posts():
    """Returns a list of post dicts from the posts/ folder."""
    make_posts_dir_if_not_exists()
    posts = []
    files = reversed(sorted(os.listdir("posts/")))
    for filename in files:
        with open("posts/" + filename) as f:
            body = Markup.escape((f.read())).replace("\n", Markup("<br />"))
        date = datetime.datetime.fromtimestamp(float(filename))
        new_post = {'date': date.strftime("%H:%M, %A %d %B %Y"), 'body': body}
        posts.append(new_post)
    return posts

def store_post(post):
    """Saves post text to a datestamped file."""
    make_posts_dir_if_not_exists()
    with open("posts/" + str(int(time.time())), "w") as f:
        f.write(post)

@app.route('/')
def index():
    """List the most recent posts, with a text box for a new post."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        posts = get_posts()[:10]
    except (ValueError, TypeError, KeyError, OSError, IOError):
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/all')
def all():
    """View all posts."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        posts = get_posts()
    except (ValueError, TypeError, KeyError, OSError, IOError):
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    """Stores a new post."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    store_post(request.form['post_body'])
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

if __name__ == '__main__':
    app.run()
