import sqlite3
import os

DATABASE_PATH = 'database/pharmacy.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Suppliers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            address TEXT,
            gst_no TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            batch_no TEXT,
            expiry_date DATE,
            quantity INTEGER DEFAULT 0,
            purchase_price REAL,
            selling_price REAL,
            supplier_id INTEGER,
            reorder_level INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            total_amount REAL,
            discount REAL DEFAULT 0,
            gst REAL DEFAULT 0,
            net_amount REAL,
            payment_method TEXT,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Sales Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    ''')
    
    # Purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            invoice_no TEXT,
            total_amount REAL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')
    
    # Purchase Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER,
            purchase_price REAL,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id),
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    ''')
    
    # Insert default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      ('admin', 'admin123', 'admin'))
    
    conn.commit()
    conn.close()