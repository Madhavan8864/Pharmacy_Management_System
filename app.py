from flask import Flask, render_template, session, redirect, url_for
from config import Config
from database.db import init_db
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.medicine_routes import medicine_bp
from routes.supplier_routes import supplier_bp
from routes.customer_routes import customer_bp
from routes.sales_routes import sales_bp
from routes.purchase_routes import purchase_bp
from routes.report_routes import report_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(medicine_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(report_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard_bp.dashboard'))
    return redirect(url_for('auth_bp.login'))

if __name__ == '__main__':
    app.run(debug=True)