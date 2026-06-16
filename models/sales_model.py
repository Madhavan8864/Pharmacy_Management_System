from database.db import get_db_connection
import datetime

class SalesModel:
    @staticmethod
    def create_sale(invoice_no, customer_id, items, discount, gst, payment_method):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calculate totals
        total_amount = sum(item['price'] * item['quantity'] for item in items)
        net_amount = total_amount + gst - discount
        
        # Insert sale
        cursor.execute('''
            INSERT INTO sales (invoice_no, customer_id, total_amount, discount, gst, net_amount, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (invoice_no, customer_id, total_amount, discount, gst, net_amount, payment_method))
        
        sale_id = cursor.lastrowid
        
        # Insert sale items and update stock
        for item in items:
            cursor.execute('''
                INSERT INTO sales_items (sale_id, medicine_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (sale_id, item['medicine_id'], item['quantity'], item['price']))
            
            # Update stock
            cursor.execute('''
                UPDATE medicines SET quantity = quantity - ? WHERE id = ?
            ''', (item['quantity'], item['medicine_id']))
        
        conn.commit()
        conn.close()
        return sale_id
    
    @staticmethod
    def get_all_sales():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, c.name as customer_name 
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            ORDER BY s.sale_date DESC
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    @staticmethod
    def get_sale_by_id(sale_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, c.name as customer_name 
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.id = ?
        ''', (sale_id,))
        sale = cursor.fetchone()
        
        if sale:
            cursor.execute('''
                SELECT si.*, m.name as medicine_name 
                FROM sales_items si
                JOIN medicines m ON si.medicine_id = m.id
                WHERE si.sale_id = ?
            ''', (sale_id,))
            items = cursor.fetchall()
            conn.close()
            return sale, items
        
        conn.close()
        return None, None
    
    @staticmethod
    def get_sales_by_date_range(start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, c.name as customer_name 
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE DATE(s.sale_date) BETWEEN ? AND ?
            ORDER BY s.sale_date DESC
        ''', (start_date, end_date))
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    @staticmethod
    def generate_invoice_number():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(invoice_no) FROM sales")
        result = cursor.fetchone()[0]
        conn.close()
        
        if result:
            num = int(result[3:]) + 1
        else:
            num = 1
        
        return f"INV{num:06d}"