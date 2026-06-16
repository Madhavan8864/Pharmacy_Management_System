from flask import Blueprint, render_template, session, redirect, url_for
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    data = DashboardController.get_dashboard_data()
    return render_template('dashboard/dashboard.html', data=data)