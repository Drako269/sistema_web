from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from database import get_db_connection
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Ruta para iniciar sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()

        if user_data and check_password_hash(user_data[1], password):
            user = User(user_data[0], username)  # Crea una instancia del modelo User
            login_user(user)  # Autentica al usuario
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.')

    return render_template('login.html')

# Ruta para cerrar sesión
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Ruta protegida (dashboard)
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Ruta para registrar nuevos usuarios
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            conn.commit()
            flash('Usuario registrado correctamente.')
        except Exception as e:
            conn.rollback()
            flash('Error al registrar el usuario.')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('auth.login'))

    return render_template('register.html')