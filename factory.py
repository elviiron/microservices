from repositories import ProductRepository, OrderRepository
from common.database import Database

class RepositoryFactory:
    def __init__(self, db):
        self.db = db

    def create_product_repository(self):
        return ProductRepository(self.db)

    def create_order_repository(self):
        return OrderRepository(self.db)

db_instance = Database()
factory = RepositoryFactory(db_instance)

product_repo = factory.create_product_repository()
order_repo = factory.create_order_repository()