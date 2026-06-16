from models.medicine_model import MedicineModel
from models.supplier_model import SupplierModel

class MedicineController:
    @staticmethod
    def add_medicine(data):
        """Add new medicine"""
        return MedicineModel.create_medicine(
            name=data['name'],
            category=data['category'],
            batch_no=data['batch_no'],
            expiry_date=data['expiry_date'],
            quantity=int(data['quantity']),
            purchase_price=float(data['purchase_price']),
            selling_price=float(data['selling_price']),
            supplier_id=int(data['supplier_id']) if data['supplier_id'] else None,
            reorder_level=int(data['reorder_level']) if data['reorder_level'] else 10
        )
    
    @staticmethod
    def update_medicine(medicine_id, data):
        """Update existing medicine"""
        MedicineModel.update_medicine(
            medicine_id=medicine_id,
            name=data['name'],
            category=data['category'],
            batch_no=data['batch_no'],
            expiry_date=data['expiry_date'],
            quantity=int(data['quantity']),
            purchase_price=float(data['purchase_price']),
            selling_price=float(data['selling_price']),
            supplier_id=int(data['supplier_id']) if data['supplier_id'] else None,
            reorder_level=int(data['reorder_level']) if data['reorder_level'] else 10
        )
    
    @staticmethod
    def delete_medicine(medicine_id):
        """Delete medicine"""
        MedicineModel.delete_medicine(medicine_id)
    
    @staticmethod
    def get_all_medicines():
        """Get all medicines as list of dictionaries"""
        medicines = MedicineModel.get_all_medicines()
        suppliers = SupplierModel.get_all_suppliers()
        
        # Convert Row objects to dict for JSON serialization
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
                'supplier_name': medicine['supplier_name'],
                'created_at': medicine['created_at']
            })
        
        # Convert suppliers to list of dictionaries
        suppliers_list = []
        for supplier in suppliers:
            suppliers_list.append({
                'id': supplier['id'],
                'name': supplier['name'],
                'contact': supplier['contact'],
                'email': supplier['email'],
                'address': supplier['address'],
                'gst_no': supplier['gst_no'],
                'created_at': supplier['created_at']
            })
        
        return medicines_list, suppliers_list
    
    @staticmethod
    def get_medicine(medicine_id):
        """Get single medicine by ID as dictionary"""
        medicine = MedicineModel.get_medicine_by_id(medicine_id)
        if medicine:
            return {
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
                'supplier_name': medicine['supplier_name'],
                'created_at': medicine['created_at']
            }
        return None
    
    @staticmethod
    def search_medicines(search_term):
        """Search medicines by name, batch or category"""
        medicines = MedicineModel.search_medicines(search_term)
        
        # Convert Row objects to dict
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
                'supplier_name': medicine['supplier_name'],
                'created_at': medicine['created_at']
            })
        return medicines_list
    
    @staticmethod
    def get_low_stock_medicines():
        """Get medicines with low stock"""
        medicines = MedicineModel.get_low_stock_medicines()
        
        # Convert Row objects to dict
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
                'reorder_level': medicine['reorder_level']
            })
        return medicines_list
    
    @staticmethod
    def update_stock(medicine_id, quantity_change):
        """Update medicine stock quantity"""
        MedicineModel.update_stock(medicine_id, quantity_change)