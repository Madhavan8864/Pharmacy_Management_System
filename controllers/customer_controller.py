from models.customer_model import CustomerModel

class CustomerController:
    @staticmethod
    def add_customer(data):
        return CustomerModel.create_customer(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address']
        )
    
    @staticmethod
    def update_customer(customer_id, data):
        CustomerModel.update_customer(
            customer_id=customer_id,
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address']
        )
    
    @staticmethod
    def delete_customer(customer_id):
        CustomerModel.delete_customer(customer_id)
    
    @staticmethod
    def get_all_customers():
        return CustomerModel.get_all_customers()
    
    @staticmethod
    def get_customer(customer_id):
        return CustomerModel.get_customer_by_id(customer_id)
    
    @staticmethod
    def search_customers(search_term):
        return CustomerModel.search_customers(search_term)