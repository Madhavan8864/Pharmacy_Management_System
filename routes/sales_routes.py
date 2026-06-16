from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from controllers.sales_controller import SalesController
from controllers.medicine_controller import MedicineController
from controllers.customer_controller import CustomerController

sales_bp = Blueprint('sales_bp', __name__, url_prefix='/sales')

@sales_bp.route('/')
def sales_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    sales = SalesController.get_all_sales()
    return render_template('sales/sales_list.html', sales=sales)

@sales_bp.route('/create', methods=['GET', 'POST'])
def create_bill():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        cart = session.get('cart', [])
        customer_id = request.form.get('customer_id')
        discount = float(request.form.get('discount', 0))
        gst = float(request.form.get('gst', 0))
        payment_method = request.form.get('payment_method')
        
        sale_id = SalesController.create_sale(cart, customer_id, discount, gst, payment_method)
        session['cart'] = []
        return redirect(url_for('sales_bp.view_invoice', sale_id=sale_id))
    
    medicines = MedicineController.get_all_medicines()[0]
    
    # Convert Row objects to dictionaries for JSON serialization
    medicines_list = []
    for medicine in medicines:
        medicines_list.append({
            'id': medicine['id'],
            'name': medicine['name'],
            'category': medicine['category'],
            'batch_no': medicine['batch_no'],
            'expiry_date': medicine['expiry_date'],
            'quantity': medicine['quantity'],
            'purchase_price': medicine['purchase_price'],
            'selling_price': medicine['selling_price'],
            'supplier_id': medicine['supplier_id'],
            'reorder_level': medicine['reorder_level'],
            'supplier_name': medicine['supplier_name']
        })
    
    customers = CustomerController.get_all_customers()
    cart = session.get('cart', [])
    
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('sales/create_bill.html', medicines=medicines_list, 
                          customers=customers, cart=cart, total=total)

@sales_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    medicine_id = int(request.form['medicine_id'])
    quantity = int(request.form['quantity'])
    
    medicine = MedicineController.get_medicine(medicine_id)
    
    if SalesController.check_stock(medicine_id, quantity):
        cart = session.get('cart', [])
        
        # Check if medicine already in cart
        found = False
        for item in cart:
            if item['medicine_id'] == medicine_id:
                item['quantity'] += quantity
                found = True
                break
        
        if not found:
            cart.append({
                'medicine_id': medicine_id,
                'name': medicine['name'],
                'quantity': quantity,
                'price': medicine['selling_price']
            })
        
        session['cart'] = cart
        return jsonify({'success': True, 'message': 'Added to cart'})
    
    return jsonify({'success': False, 'message': 'Insufficient stock'})

@sales_bp.route('/remove-from-cart/<int:medicine_id>')
def remove_from_cart(medicine_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['medicine_id'] != medicine_id]
    session['cart'] = cart
    return redirect(url_for('sales_bp.create_bill'))

@sales_bp.route('/clear-cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('sales_bp.create_bill'))

@sales_bp.route('/invoice/<int:sale_id>')
def view_invoice(sale_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    sale, items = SalesController.get_sale(sale_id)
    return render_template('sales/invoice.html', sale=sale, items=items)