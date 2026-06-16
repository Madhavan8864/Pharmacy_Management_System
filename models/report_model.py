from database.db import get_db_connection

class ReportModel:
    @staticmethod
    def get_sales_summary(start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as total_sales,
                SUM(net_amount) as total_revenue,
                SUM(total_amount) as total_amount_before_tax,
                SUM(discount) as total_discount,
                SUM(gst) as total_gst,
                AVG(net_amount) as avg_sale_value
            FROM sales
            WHERE DATE(sale_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        summary = cursor.fetchone()
        conn.close()
        return summary
    
    @staticmethod
    def get_sales_by_date_range(start_date, end_date):
        """Get all sales within date range"""
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
        
        # Convert to list of dictionaries
        sales_list = []
        for sale in sales:
            sales_list.append({
                'id': sale['id'],
                'invoice_no': sale['invoice_no'],
                'customer_id': sale['customer_id'],
                'customer_name': sale['customer_name'],
                'total_amount': sale['total_amount'],
                'discount': sale['discount'],
                'gst': sale['gst'],
                'net_amount': sale['net_amount'],
                'payment_method': sale['payment_method'],
                'sale_date': sale['sale_date']
            })
        return sales_list
    
    @staticmethod
    def get_top_medicines(start_date, end_date, limit=10):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.name,
                m.category,
                SUM(si.quantity) as total_quantity,
                SUM(si.quantity * si.price) as total_revenue
            FROM sales_items si
            JOIN medicines m ON si.medicine_id = m.id
            JOIN sales s ON si.sale_id = s.id
            WHERE DATE(s.sale_date) BETWEEN ? AND ?
            GROUP BY si.medicine_id
            ORDER BY total_quantity DESC
            LIMIT ?
        ''', (start_date, end_date, limit))
        medicines = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        medicines_list = []
        for medicine in medicines:
            medicines_list.append({
                'name': medicine['name'],
                'category': medicine['category'],
                'total_quantity': medicine['total_quantity'],
                'total_revenue': medicine['total_revenue']
            })
        return medicines_list
    
    @staticmethod
    def get_stock_report():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                m.*,
                s.name as supplier_name,
                (m.quantity * m.selling_price) as stock_value
            FROM medicines m
            LEFT JOIN suppliers s ON m.supplier_id = s.id
            ORDER BY m.quantity ASC
        ''')
        stock = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        stock_list = []
        for item in stock:
            stock_list.append({
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'batch_no': item['batch_no'],
                'expiry_date': item['expiry_date'],
                'quantity': item['quantity'],
                'purchase_price': item['purchase_price'],
                'selling_price': item['selling_price'],
                'supplier_id': item['supplier_id'],
                'supplier_name': item['supplier_name'],
                'reorder_level': item['reorder_level'],
                'stock_value': item['stock_value']
            })
        return stock_list
    
    @staticmethod
    def get_expiry_report():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM medicines 
            WHERE expiry_date <= DATE('now', '+30 days')
            ORDER BY expiry_date ASC
        ''')
        expiring = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        expiring_list = []
        for item in expiring:
            expiring_list.append({
                'id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'batch_no': item['batch_no'],
                'expiry_date': item['expiry_date'],
                'quantity': item['quantity'],
                'purchase_price': item['purchase_price'],
                'selling_price': item['selling_price']
            })
        return expiring_list
    
    @staticmethod
    def get_profit_report(start_date, end_date):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                SUM(si.quantity * (si.price - m.purchase_price)) as total_profit
            FROM sales_items si
            JOIN medicines m ON si.medicine_id = m.id
            JOIN sales s ON si.sale_id = s.id
            WHERE DATE(s.sale_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        profit = cursor.fetchone()
        conn.close()
        return profit[0] if profit and profit[0] else 0