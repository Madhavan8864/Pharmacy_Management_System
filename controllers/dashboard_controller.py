from models.medicine_model import MedicineModel
from models.sales_model import SalesModel
from database.db import get_db_connection
import datetime

class DashboardController:
    @staticmethod
    def get_dashboard_data():
        medicines = MedicineModel.get_all_medicines()
        low_stock = MedicineModel.get_low_stock_medicines()
        sales = SalesModel.get_all_sales()
        
        # Today's sales
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_sales = [s for s in sales if s['sale_date'].startswith(today)]
        
        total_medicines = len(medicines)
        total_stock_value = sum(m['quantity'] * m['selling_price'] for m in medicines if m['selling_price'])
        
        total_today_sales = sum(s['net_amount'] for s in today_sales)
        total_today_transactions = len(today_sales)
        
        # Expiring medicines
        expiring = []
        for m in medicines:
            if m['expiry_date']:
                try:
                    expiry_date = datetime.datetime.strptime(m['expiry_date'], '%Y-%m-%d').date()
                    if expiry_date <= datetime.date.today() + datetime.timedelta(days=30):
                        expiring.append(m)
                except:
                    pass
        
        return {
            'total_medicines': total_medicines,
            'total_stock_value': total_stock_value,
            'total_today_sales': total_today_sales,
            'total_today_transactions': total_today_transactions,
            'low_stock_count': len(low_stock),
            'expiring_count': len(expiring),
            'low_stock_medicines': low_stock,
            'expiring_medicines': expiring,
            'recent_sales': sales[:5]
        }