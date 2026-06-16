from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.customer_controller import CustomerController

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/customers')

@customer_bp.route('/')
def customer_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    customers = CustomerController.get_all_customers()
    return render_template('customer/customer_list.html', customers=customers)

@customer_bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        CustomerController.add_customer(request.form)
        return redirect(url_for('customer_bp.customer_list'))
    
    return render_template('customer/add_customer.html')

@customer_bp.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        CustomerController.update_customer(customer_id, request.form)
        return redirect(url_for('customer_bp.customer_list'))
    
    customer = CustomerController.get_customer(customer_id)
    return render_template('customer/customer_view.html', customer=customer)

@customer_bp.route('/delete/<int:customer_id>')
def delete_customer(customer_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    CustomerController.delete_customer(customer_id)
    return redirect(url_for('customer_bp.customer_list'))

@customer_bp.route('/search')
def search_customers():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    search_term = request.args.get('search', '')
    customers = CustomerController.search_customers(search_term)
    return render_template('customer/customer_list.html', customers=customers, search_term=search_term)