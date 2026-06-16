from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.supplier_controller import SupplierController

supplier_bp = Blueprint('supplier_bp', __name__, url_prefix='/suppliers')

@supplier_bp.route('/')
def supplier_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    suppliers = SupplierController.get_all_suppliers()
    return render_template('supplier/supplier_list.html', suppliers=suppliers)

@supplier_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        SupplierController.add_supplier(request.form)
        return redirect(url_for('supplier_bp.supplier_list'))
    
    return render_template('supplier/add_supplier.html')

@supplier_bp.route('/edit/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        SupplierController.update_supplier(supplier_id, request.form)
        return redirect(url_for('supplier_bp.supplier_list'))
    
    supplier = SupplierController.get_supplier(supplier_id)
    return render_template('supplier/edit_supplier.html', supplier=supplier)

@supplier_bp.route('/delete/<int:supplier_id>')
def delete_supplier(supplier_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    SupplierController.delete_supplier(supplier_id)
    return redirect(url_for('supplier_bp.supplier_list'))