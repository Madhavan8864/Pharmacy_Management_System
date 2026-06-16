from models.report_model import ReportModel

class ReportController:
    @staticmethod
    def get_sales_report(start_date, end_date):
        summary = ReportModel.get_sales_summary(start_date, end_date)
        top_medicines = ReportModel.get_top_medicines(start_date, end_date)
        sales = ReportModel.get_sales_by_date_range(start_date, end_date)  # Need to import
        profit = ReportModel.get_profit_report(start_date, end_date)
        
        return {
            'summary': summary,
            'top_medicines': top_medicines,
            'sales': sales,
            'profit': profit
        }
    
    @staticmethod
    def get_stock_report():
        return ReportModel.get_stock_report()
    
    @staticmethod
    def get_expiry_report():
        return ReportModel.get_expiry_report()