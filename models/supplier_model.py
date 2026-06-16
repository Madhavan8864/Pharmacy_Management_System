from database.db import get_db_connection

class SupplierModel:
    @staticmethod
    def create_supplier(name, contact, email, address, gst_no):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO suppliers (name, contact, email, address, gst_no)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, contact, email, address, gst_no))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    @staticmethod
    def get_all_suppliers():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers ORDER BY name")
        suppliers = cursor.fetchall()
        conn.close()
        return suppliers
    
    @staticmethod
    def get_supplier_by_id(supplier_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        supplier = cursor.fetchone()
        conn.close()
        return supplier
    
    @staticmethod
    def update_supplier(supplier_id, name, contact, email, address, gst_no):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers 
            SET name=?, contact=?, email=?, address=?, gst_no=?
            WHERE id=?
        ''', (name, contact, email, address, gst_no, supplier_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_supplier(supplier_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
        conn.commit()
        conn.close()