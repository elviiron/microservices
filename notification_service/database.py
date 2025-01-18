import sqlite3

class Database:
    def __init__(self, db_name='inspiregirl.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.create_orders_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category_name TEXT,
                description TEXT,
                price REAL,
                image_url TEXT
            )
        ''')
        self.connection.commit()

    def create_orders_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city TEXT,
                address TEXT,
                email TEXT,
                products TEXT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def insert_product(self, category_name, description, price, image_url):
        self.cursor.execute('''
            INSERT INTO products (category_name, description, price, image_url)
            VALUES (?, ?, ?, ?)
        ''', (category_name, description, price, image_url))
        self.connection.commit()

    def insert_order(self, name, city, address, email, products):
        self.cursor.execute('''
            INSERT INTO orders (name, city, address, email, products)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, city, address, email, products))
        self.connection.commit()

    def fetch_all_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id):
        self.cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return self.cursor.fetchone()

    def fetch_products_by_category(self, category_name):
        self.cursor.execute('SELECT * FROM products WHERE category_name = ?', (category_name,))
        return self.cursor.fetchall()

    def fetch_all_categories(self):
        self.cursor.execute('SELECT DISTINCT category_name FROM products')
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        self.connection.close()

    def clear_products(self):
        self.cursor.execute("DELETE FROM products")
        self.connection.commit()
