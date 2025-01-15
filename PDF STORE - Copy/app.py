from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

app = Flask(__name__)

# Configuring MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'  # Replace with your MySQL server address
app.config['MYSQL_USER'] = 'Devil.Dadu'       # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'A06140902@@b'       # Replace with your MySQL password
app.config['MYSQL_DB'] = 'pdf_store'
app.secret_key = 'your_secret_key_here'

# Initialize MySQL and LoginManager
mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Admin model (user authentication)
class Admin(UserMixin):
    def __init__(self, id):
        self.id = id

# Load admin from the database
@login_manager.user_loader
def load_admin(admin_id):
    return Admin(admin_id)

# Home page that lists all PDFs
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pdfs")
    pdfs = cur.fetchall()
    return render_template('index.html', pdf_files=pdfs)

# Admin login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", [username])
        admin = cur.fetchone()

        if admin and bcrypt.checkpw(password.encode('utf-8'), admin[2].encode('utf-8')):  # password is hashed
            user = Admin(admin[0])
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Failed. Check your username and/or password.', 'danger')

    return render_template('login.html')

# Admin dashboard where PDFs can be managed
@app.route('/admin')
@login_required
def admin_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pdfs")
    pdfs = cur.fetchall()
    return render_template('admin_dashboard.html', pdf_files=pdfs)

# Route to add new PDFs from admin panel
@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_pdf():
    if request.method == 'POST':
        name = request.form['name']
        filename = request.form['filename']
        price = request.form['price']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pdfs (name, filename, price) VALUES (%s, %s, %s)", (name, filename, price))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_pdf.html')

# Route to delete a PDF
@app.route('/admin/delete/<int:pdf_id>')
@login_required
def delete_pdf(pdf_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pdfs WHERE id = %s", [pdf_id])
    mysql.connection.commit()
    return redirect(url_for('admin_dashboard'))

# Admin logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
