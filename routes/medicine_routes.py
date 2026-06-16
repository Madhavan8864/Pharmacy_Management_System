from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers.medicine_controller import MedicineController

medicine_bp = Blueprint('medicine_bp', __name__, url_prefix='/medicines')

@medicine_bp.route('/')
def medicine_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    medicines, suppliers = MedicineController.get_all_medicines()
    return render_template('medicine/medicine_list.html', medicines=medicines, suppliers=suppliers)

@medicine_bp.route('/add', methods=['GET', 'POST'])
def add_medicine():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        MedicineController.add_medicine(request.form)
        return redirect(url_for('medicine_bp.medicine_list'))
    
    from controllers.supplier_controller import SupplierController
    suppliers = SupplierController.get_all_suppliers()
    return render_template('medicine/add_medicine.html', suppliers=suppliers)

@medicine_bp.route('/edit/<int:medicine_id>', methods=['GET', 'POST'])
def edit_medicine(medicine_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        MedicineController.update_medicine(medicine_id, request.form)
        return redirect(url_for('medicine_bp.medicine_list'))
    
    medicine = MedicineController.get_medicine(medicine_id)
    from controllers.supplier_controller import SupplierController
    suppliers = SupplierController.get_all_suppliers()
    return render_template('medicine/edit_medicine.html', medicine=medicine, suppliers=suppliers)

@medicine_bp.route('/delete/<int:medicine_id>')
def delete_medicine(medicine_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    MedicineController.delete_medicine(medicine_id)
    return redirect(url_for('medicine_bp.medicine_list'))

@medicine_bp.route('/view/<int:medicine_id>')
def view_medicine(medicine_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    medicine = MedicineController.get_medicine(medicine_id)
    return render_template('medicine/medicine_view.html', medicine=medicine)

@medicine_bp.route('/search')
def search_medicines():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    search_term = request.args.get('search', '')
    medicines = MedicineController.search_medicines(search_term)
    return render_template('medicine/medicine_list.html', medicines=medicines, search_term=search_term)