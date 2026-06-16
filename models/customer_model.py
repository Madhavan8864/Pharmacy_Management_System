from database.db import get_db_connection

class CustomerModel:
    @staticmethod
    def create_customer(name, phone, email, address):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, phone, email, address)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, email, address))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    @staticmethod
    def get_all_customers():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY name")
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    @staticmethod
    def get_customer_by_id(customer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer
    
    @staticmethod
    def update_customer(customer_id, name, phone, email, address):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers 
            SET name=?, phone=?, email=?, address=?
            WHERE id=?
        ''', (name, phone, email, address, customer_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_customer(customer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def search_customers(search_term):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        customers = cursor.fetchall()
        conn.close()
        return customers