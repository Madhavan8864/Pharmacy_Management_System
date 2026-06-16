from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from controllers.purchase_controller import PurchaseController
from controllers.medicine_controller import MedicineController
from controllers.supplier_controller import SupplierController

purchase_bp = Blueprint('purchase_bp', __name__, url_prefix='/purchases')

@purchase_bp.route('/')
def purchase_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    purchases = PurchaseController.get_all_purchases()
    return render_template('purchase/purchase_list.html', purchases=purchases)

@purchase_bp.route('/add', methods=['GET', 'POST'])
def add_purchase():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id')
        invoice_no = request.form.get('invoice_no')
        
        # Process purchase items
        medicine_ids = request.form.getlist('medicine_id')
        quantities = request.form.getlist('quantity')
        purchase_prices = request.form.getlist('purchase_price')
        
        items = []
        for i in range(len(medicine_ids)):
            if medicine_ids[i] and quantities[i] and purchase_prices[i]:
                items.append({
                    'medicine_id': int(medicine_ids[i]),
                    'quantity': int(quantities[i]),
                    'purchase_price': float(purchase_prices[i])
                })
        
        PurchaseController.create_purchase(supplier_id, invoice_no, items)
        return redirect(url_for('purchase_bp.purchase_list'))
    
    suppliers = SupplierController.get_all_suppliers()
    medicines = MedicineController.get_all_medicines()[0]
    return render_template('purchase/add_purchase.html', suppliers=suppliers, medicines=medicines)