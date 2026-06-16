from models.purchase_model import PurchaseModel

class PurchaseController:
    @staticmethod
    def create_purchase(supplier_id, invoice_no, items):
        return PurchaseModel.create_purchase(supplier_id, invoice_no, items)
    
    @staticmethod
    def get_all_purchases():
        return PurchaseModel.get_all_purchases()
    
    @staticmethod
    def get_purchase(purchase_id):
        return PurchaseModel.get_purchase_by_id(purchase_id)