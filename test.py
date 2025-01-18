import unittest
from common.database import Database

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Database(':memory:')

    def setUp(self):
        self.db.clear_products()


    def test_create_table(self):
        products = self.db.fetch_all_products()
        self.assertEqual(products, [])

    def test_insert_product(self):
        product_data = ('Платья', 'INSPIRE САРАФАН ДЛИНЫ МИДИ С ЗАВЯЗКАМИ НА СПИНЕ (БЕЛЫЙ)', '2 990 ₽',
                       'https://inspireshop.ru/upload/resize_cache/webp/upload/iblock/bcb/b77s2876nccrw2s7uem256fmca90f52e.webp')
        self.db.insert_product(*product_data)

        products = self.db.fetch_all_products()
        print(products)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1:], product_data)




    def test_get_product_by_id(self):
        product_data = ('Платья', 'INSPIRE САРАФАН ДЛИНЫ МИДИ С ЗАВЯЗКАМИ НА СПИНЕ (БЕЛЫЙ)', '2 990 ₽', 
                       'https://inspireshop.ru/upload/resize_cache/webp/upload/iblock/bcb/b77s2876nccrw2s7uem256fmca90f52e.webp')
        self.db.insert_product(*product_data)

        product = self.db.get_product_by_id(1)
        self.assertIsNotNone(product)
        self.assertEqual(product[1:], product_data)

    def test_fetch_products_by_category(self):
        product_data_1 = ('Платья', 'INSPIRE САРАФАН ДЛИНЫ МИДИ С ЗАВЯЗКАМИ НА СПИНЕ (БЕЛЫЙ)', '2 990 ₽', 
                         'https://inspireshop.ru/upload/resize_cache/webp/upload/iblock/bcb/b77s2876nccrw2s7uem256fmca90f52e.webp')
        product_data_2 = ('Брюки', 'INSPIRE БРЮКИ-ДЖОГГЕРЫ УТЕПЛЕННЫЕ С НАЧЕСОМ INSPIRE CLUB (ТЕМНО-СИНИЙ)', '8 590 ₽',
                         'https://inspireshop.ru/upload/resize_cache/webp/iblock/9b5/t4h15qt3kald23plvq80fekn8slu7akn.webp')
        self.db.insert_product(*product_data_1)
        self.db.insert_product(*product_data_2)

        products = self.db.fetch_products_by_category('Брюки')
        print(products)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1:], product_data_2)

    def test_fetch_all_categories(self):
        product_data_1 = ('Платья', 'INSPIRE САРАФАН ДЛИНЫ МИДИ С ЗАВЯЗКАМИ НА СПИНЕ (БЕЛЫЙ)', '2 990 ₽',
                          'https://inspireshop.ru/upload/resize_cache/webp/upload/iblock/bcb/b77s2876nccrw2s7uem256fmca90f52e.webp')
        product_data_2 = ('Брюки', 'INSPIRE БРЮКИ-ДЖОГГЕРЫ УТЕПЛЕННЫЕ С НАЧЕСОМ INSPIRE CLUB (ТЕМНО-СИНИЙ)', '8 590 ₽',
                          'https://inspireshop.ru/upload/resize_cache/webp/iblock/9b5/t4h15qt3kald23plvq80fekn8slu7akn.webp')
        self.db.insert_product(*product_data_1)
        self.db.insert_product(*product_data_2)

        categories = self.db.fetch_all_categories()
        self.assertEqual(len(categories), 2)
        self.assertIn('Платья', categories)
        self.assertIn('Брюки', categories)


    def closeClass(cls):
        cls.db.close()

if __name__ == '__main__':
    unittest.main()




