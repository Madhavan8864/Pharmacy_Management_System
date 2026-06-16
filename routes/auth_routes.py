from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = AuthController.login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            return render_template('auth/login.html', error='Invalid credentials')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'staff')
        
        user_id = AuthController.register_user(username, password, role)
        if user_id:
            return redirect(url_for('auth_bp.login'))
        else:
            return render_template('auth/register.html', error='Username already exists')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))