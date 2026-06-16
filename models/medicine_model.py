from database.db import get_db_connection

class MedicineModel:
    @staticmethod
    def create_medicine(name, category, batch_no, expiry_date, quantity, 
                       purchase_price, selling_price, supplier_id, reorder_level=10):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medicines (name, category, batch_no, expiry_date, quantity,
                                 purchase_price, selling_price, supplier_id, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, batch_no, expiry_date, quantity, purchase_price, 
              selling_price, supplier_id, reorder_level))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    @staticmethod
    def get_all_medicines():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.name as supplier_name 
            FROM medicines m
            LEFT JOIN suppliers s ON m.supplier_id = s.id
            ORDER BY m.name
        ''')
        medicines = cursor.fetchall()
        conn.close()
        return medicines
    
    @staticmethod
    def get_medicine_by_id(medicine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.name as supplier_name 
            FROM medicines m
            LEFT JOIN suppliers s ON m.supplier_id = s.id
            WHERE m.id = ?
        ''', (medicine_id,))
        medicine = cursor.fetchone()
        conn.close()
        return medicine
    
    @staticmethod
    def update_medicine(medicine_id, name, category, batch_no, expiry_date, 
                       quantity, purchase_price, selling_price, supplier_id, reorder_level):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE medicines 
            SET name=?, category=?, batch_no=?, expiry_date=?, quantity=?,
                purchase_price=?, selling_price=?, supplier_id=?, reorder_level=?
            WHERE id=?
        ''', (name, category, batch_no, expiry_date, quantity, purchase_price, 
              selling_price, supplier_id, reorder_level, medicine_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_medicine(medicine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_stock(medicine_id, quantity_change):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE medicines SET quantity = quantity + ? WHERE id=?", 
                      (quantity_change, medicine_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def search_medicines(search_term):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, s.name as supplier_name 
            FROM medicines m
            LEFT JOIN suppliers s ON m.supplier_id = s.id
            WHERE m.name LIKE ? OR m.batch_no LIKE ? OR m.category LIKE ?
            ORDER BY m.name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        medicines = cursor.fetchall()
        conn.close()
        return medicines
    
    @staticmethod
    def get_low_stock_medicines():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM medicines 
            WHERE quantity <= reorder_level
            ORDER BY quantity ASC
        ''')
        medicines = cursor.fetchall()
        conn.close()
        return medicines