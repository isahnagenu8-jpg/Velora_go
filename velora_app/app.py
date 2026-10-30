from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-before-deploying')
DB = os.path.join(os.path.dirname(__file__), 'velora.db')

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, kind TEXT NOT NULL, title TEXT NOT NULL, details TEXT, price TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))''')

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'info')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    return render_template('index.html', user=session.get('name'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or len(password) < 8:
            flash('Enter your name and email, and use a password of at least 8 characters.', 'error')
            return render_template('auth.html', mode='signup')
        try:
            with db() as conn:
                cur = conn.execute('INSERT INTO users(name,email,password) VALUES(?,?,?)', (name, email, generate_password_hash(password)))
                session['user_id'], session['name'] = cur.lastrowid, name
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash('That email already has an account. Try logging in.', 'error')
    return render_template('auth.html', mode='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        with db() as conn:
            user = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'], session['name'] = user['id'], user['name']
            return redirect(url_for('home'))
        flash('Email or password is incorrect.', 'error')
    return render_template('auth.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/book', methods=['POST'])
@login_required
def book():
    data = request.get_json(silent=True) or {}
    kind, title = data.get('kind', ''), data.get('title', '').strip()
    details, price = data.get('details', '').strip(), data.get('price', '').strip()
    if kind not in ('ride', 'stay') or not title:
        return jsonify(ok=False, message='Please provide valid booking details.'), 400
    with db() as conn:
        conn.execute('INSERT INTO bookings(user_id,kind,title,details,price) VALUES(?,?,?,?,?)', (session['user_id'], kind, title, details, price))
    return jsonify(ok=True, message='Booking saved to your dashboard.')

@app.route('/dashboard')
@login_required
def dashboard():
    with db() as conn:
        bookings = conn.execute('SELECT * FROM bookings WHERE user_id=? ORDER BY id DESC', (session['user_id'],)).fetchall()
    return render_template('dashboard.html', user=session.get('name'), bookings=bookings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
