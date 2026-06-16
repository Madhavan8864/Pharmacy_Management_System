from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.report_controller import ReportController
import datetime

report_bp = Blueprint('report_bp', __name__, url_prefix='/reports')

@report_bp.route('/sales')
def sales_report():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    start_date = request.args.get('start_date', datetime.date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.date.today().strftime('%Y-%m-%d'))
    
    report_data = ReportController.get_sales_report(start_date, end_date)
    return render_template('reports/sales_report.html', 
                          report=report_data, 
                          start_date=start_date, 
                          end_date=end_date)

@report_bp.route('/stock')
def stock_report():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    stock = ReportController.get_stock_report()
    return render_template('reports/stock_report.html', stock=stock)

@report_bp.route('/revenue')
def revenue_report():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    start_date = request.args.get('start_date', datetime.date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.date.today().strftime('%Y-%m-%d'))
    
    report_data = ReportController.get_sales_report(start_date, end_date)
    return render_template('reports/revenue_report.html', 
                          report=report_data, 
                          start_date=start_date, 
                          end_date=end_date)