import sqlite3

class Database:
    _instance = None

    def __new__(cls, db_name=r"C:\Users\Lenovo\PycharmProjects\pythonProject2\inspiregirl.db"):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name, check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.create_table()
            cls._instance.create_orders_table()
        return cls._instance

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
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM products")
        self.connection.commit()