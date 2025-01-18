

class ProductRepository:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        self.db.create_table()

    def insert_product(self, category_name, description, price, image_url):
        self.db.insert_product(category_name, description, price, image_url)

    def fetch_all_products(self):
        return self.db.fetch_all_products()

    def fetch_products_by_category(self, category_name):
        return self.db.fetch_products_by_category(category_name)

    def fetch_all_categories(self):
        return self.db.fetch_all_categories()

    def get_product_by_id(self, product_id):
        return self.db.get_product_by_id(product_id)

