from models.sales_model import SalesModel
from models.medicine_model import MedicineModel

class SalesController:
    @staticmethod
    def create_sale(cart_items, customer_id, discount, gst, payment_method):
        invoice_no = SalesModel.generate_invoice_number()
        return SalesModel.create_sale(invoice_no, customer_id, cart_items, discount, gst, payment_method)
    
    @staticmethod
    def get_all_sales():
        return SalesModel.get_all_sales()
    
    @staticmethod
    def get_sale(sale_id):
        return SalesModel.get_sale_by_id(sale_id)
    
    @staticmethod
    def check_stock(medicine_id, quantity):
        medicine = MedicineModel.get_medicine_by_id(medicine_id)
        if medicine and medicine['quantity'] >= quantity:
            return True
        return False