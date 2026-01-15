from flask import Flask, request, render_template, redirect, url_for, session, send_file
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'insecure_secret_key'  # Insecure

# Database setup
def init_db():
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password')")
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'pass')")
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('adomin', 'adominpass')")
    c.execute('CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, name TEXT, energy TEXT, power_fiscal INTEGER, power_max INTEGER, transmission TEXT, price INTEGER, image TEXT)')
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 CRDi 134 Prestige BVA', 'Diesel', 6, 134, 'Automatique 7 rapports à double embrayage', 359900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Prestige')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 T-GDi HEV 230 Premium', 'Hybride', 9, 230, 'Automatique 6 rapports à double embrayage', 379900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Premium')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 CRDi 134 Premium BVA', 'Diesel', 6, 134, 'Automatique 7 rapports à double embrayage', 379900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Premium+Diesel')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 T-GDi HEV 230 Luxe', 'Hybride', 9, 230, 'Automatique 6 rapports à double embrayage', 414900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Luxe')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 CRDi 134 Luxe BVA', 'Diesel', 6, 134, 'Automatique 7 rapports à double embrayage', 414900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Luxe+Diesel')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 T-GDi HEV 230 Ultimate', 'Hybride', 9, 230, 'Automatique 6 rapports à double embrayage', 444900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Ultimate')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 CRDi 134 Ultimate BVA', 'Diesel', 6, 134, 'Automatique 7 rapports à double embrayage', 444900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+Ultimate+Diesel')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 T-GDi HEV 230 N-Line', 'Hybride', 9, 230, 'Automatique 6 rapports à double embrayage', 464900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+N-Line')")
    c.execute("INSERT OR IGNORE INTO cars (name, energy, power_fiscal, power_max, transmission, price, image) VALUES ('Hyundai Tucson 1.6 CRDi 134 N-Line BVA', 'Diesel', 6, 134, 'Automatique 7 rapports à double embrayage', 464900, 'https://via.placeholder.com/300x200?text=Hyundai+Tucson+N-Line+Diesel')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # Vulnerable to SQL injection
    c.execute(query)
    user = c.fetchone()
    conn.close()
    if user:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid credentials'

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars")
    cars = c.fetchall()
    conn.close()
    return render_template('dashboard.html', cars=cars)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    results = []
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('vulnerable.db')
        c = conn.cursor()
        # Vulnerable to SQL injection
        sql = f"SELECT * FROM cars WHERE name LIKE '%{query}%'"
        c.execute(sql)
        results = c.fetchall()
        conn.close()
    return render_template('search.html', results=results)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join('uploads', filename))  # No validation
            return 'File uploaded'
    return render_template('upload.html')

@app.route('/checkout/<int:car_id>', methods=['GET', 'POST'])
def checkout(car_id):
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    conn = sqlite3.connect('vulnerable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    car = c.fetchone()
    conn.close()
    if not car:
        return 'Car not found'
    if request.method == 'POST':
        # Simulate payment
        return 'Payment successful! Thank you for your purchase.'
    return render_template('checkout.html', car=car)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)