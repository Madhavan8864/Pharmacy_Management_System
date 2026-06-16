from database.db import get_db_connection

class PurchaseModel:
    @staticmethod
    def create_purchase(supplier_id, invoice_no, items):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        total_amount = sum(item['quantity'] * item['purchase_price'] for item in items)
        
        cursor.execute('''
            INSERT INTO purchases (supplier_id, invoice_no, total_amount)
            VALUES (?, ?, ?)
        ''', (supplier_id, invoice_no, total_amount))
        
        purchase_id = cursor.lastrowid
        
        for item in items:
            cursor.execute('''
                INSERT INTO purchase_items (purchase_id, medicine_id, quantity, purchase_price)
                VALUES (?, ?, ?, ?)
            ''', (purchase_id, item['medicine_id'], item['quantity'], item['purchase_price']))
            
            # Update stock and purchase price
            cursor.execute('''
                UPDATE medicines 
                SET quantity = quantity + ?, purchase_price = ?
                WHERE id = ?
            ''', (item['quantity'], item['purchase_price'], item['medicine_id']))
        
        conn.commit()
        conn.close()
        return purchase_id
    
    @staticmethod
    def get_all_purchases():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, s.name as supplier_name 
            FROM purchases p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            ORDER BY p.purchase_date DESC
        ''')
        purchases = cursor.fetchall()
        conn.close()
        return purchases
    
    @staticmethod
    def get_purchase_by_id(purchase_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, s.name as supplier_name 
            FROM purchases p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.id = ?
        ''', (purchase_id,))
        purchase = cursor.fetchone()
        
        if purchase:
            cursor.execute('''
                SELECT pi.*, m.name as medicine_name 
                FROM purchase_items pi
                JOIN medicines m ON pi.medicine_id = m.id
                WHERE pi.purchase_id = ?
            ''', (purchase_id,))
            items = cursor.fetchall()
            conn.close()
            return purchase, items
        
        conn.close()
        return None, None