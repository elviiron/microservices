from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from repositories import ProductRepository
import requests


class App(Flask):
    def __init__(self, name):
        super().__init__(name)
        self.secret_key = 'my_secret_key'
        self.db = Database()
        self.product_repo = ProductRepository(self.db)
        self.product_repo.create_table()
        self.register_routes()


    def register_routes(self):
        @self.route('/')
        def index():
            categories = self.product_repo.fetch_all_categories()  
            return render_template('index.html', categories=categories)

        @self.route('/Каталог/<string:category_name>', methods=['GET', 'POST'])
        def category(category_name):
            categories = self.product_repo.fetch_all_categories() 
            products = self.product_repo.fetch_products_by_category(category_name)  

            if request.method == 'POST':
                product_id = request.form.get('product_id')
                product = self.product_repo.get_product_by_id(product_id)
                if product:
                    if 'basket' not in session:
                        session['basket'] = []
                        session['basket'].append({
                                                 'id': product[0],                        
                                                 'title': product[2],                        
                                                 'price': product[3],                       
                                                  'img_src': product[4]
                        })
                        session.modified = True
                return redirect(url_for('category', category_name=category_name))
            return render_template('category.html', products=products, categories=categories, category_name=category_name)
        
        @self.route('/basket', methods=['GET', 'POST'])
        def basket():
            if request.method == 'POST':
                product_id = int(request.form.get('product_id'))
                if 'basket' in session:
                    session['basket'] = [item for item in session['basket'] if item['id'] != product_id]
                    session.modified = True
                return redirect(url_for('basket'))
            return render_template('basket.html', cart=session.get('basket', []))
        
        @self.route('/checkout', methods=['POST'])
        def checkout():
            if 'basket' not in session or not session['basket']:
                return redirect(url_for('basket'))

            order_data = {
                'name': request.form.get('name'),
                'city': request.form.get('city'),
                'address': request.form.get('address'),
                'email': request.form.get('email'),
                'basket': session['basket']
            }

            response = requests.post('http://notification_service:5000/place_order', json=order_data)

            if response.status_code == 200:
                return render_template('order_successful.html')
            else:
                return f"Ошибка при оформлении заказа: {response.text}", response.status_code


if __name__ == '__main__':
    app_instance = App(__name__)
    app_instance.run(host='0.0.0.0', port=5000)
