from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from common.database import Database

class Parser:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--headless")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)

        self.urls = [
            'https://inspireshop.ru/catalog/platya/',
            'https://inspireshop.ru/catalog/svitshoty_i_longslivy/',
            'https://inspireshop.ru/catalog/bryuki/'
        ]
        self.db = Database()

    def parse(self):
        for url in self.urls:
            self.driver.get(url)
            category_element = self.driver.find_element(By.CSS_SELECTOR, 'ol.breadcrumb li:last-child span[itemprop="name"]')
            category_name = category_element.text.strip()
            print(f'Извлеченная категория: {category_name}')

            found_goods = self.driver.find_elements(By.CLASS_NAME, 'product-item-container')
            for item in found_goods:
                title_element = item.find_element(By.CLASS_NAME, 'sp-productitem-title')
                title = title_element.text.strip()
                price_element = item.find_element(By.CLASS_NAME, 'product-item-price-container')
                price = price_element.text.strip()
                img_element = item.find_element(By.CSS_SELECTOR, 'img.sp-productitem-firstPic')
                img_src = img_element.get_attribute('src')
                self.db.insert_product(category_name, title, price, img_src)
                print(category_name, title, price, img_src)  

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    parser.close()