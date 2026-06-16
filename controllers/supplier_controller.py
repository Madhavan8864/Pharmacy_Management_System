from models.supplier_model import SupplierModel

class SupplierController:
    @staticmethod
    def add_supplier(data):
        return SupplierModel.create_supplier(
            name=data['name'],
            contact=data['contact'],
            email=data['email'],
            address=data['address'],
            gst_no=data['gst_no']
        )
    
    @staticmethod
    def update_supplier(supplier_id, data):
        SupplierModel.update_supplier(
            supplier_id=supplier_id,
            name=data['name'],
            contact=data['contact'],
            email=data['email'],
            address=data['address'],
            gst_no=data['gst_no']
        )
    
    @staticmethod
    def delete_supplier(supplier_id):
        SupplierModel.delete_supplier(supplier_id)
    
    @staticmethod
    def get_all_suppliers():
        return SupplierModel.get_all_suppliers()
    
    @staticmethod
    def get_supplier(supplier_id):
        return SupplierModel.get_supplier_by_id(supplier_id)