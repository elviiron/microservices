from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from database import Database
from repositories import ProductRepository, OrderRepository
from facade import OrderFacade


class NotificationService(Flask):
    def __init__(self, name):
        super().__init__(name, template_folder='../templates', static_folder='../static')
        self.secret_key = 'my_secret_key'
        self.db = Database()
        self.product_repo = ProductRepository(self.db)
        self.order_repo = OrderRepository(self.db)
        self.product_repo.create_table()
        self.order_repo.create_orders_table()
        self.order_facade = OrderFacade(self.order_repo, self)
    
        self.config['MAIL_SERVER'] = 'smtp.mail.ru'
        self.config['MAIL_PORT'] = 465
        self.config['MAIL_USERNAME'] = 'elyayazah@mail.ru'
        self.config['MAIL_PASSWORD'] = '5nUUe2utP5x8CqRB1WnF'
        self.config['MAIL_USE_TLS'] = False
        self.config['MAIL_USE_SSL'] = True
        self.config['MAIL_DEFAULT_SENDER'] = 'elyayazah@mail.ru'
        self.mail = Mail(self)
        self.register_routes()

    def send_order_confirmation(self, email, name, address, city, product_list_str):
        msg = Message("Заказ оформлен", recipients=[email])
        msg.body = (
            f"Спасибо за ваш заказ, {name}! "
            f"Ваш адрес: {address}, {city}. "
            f"Содержимое заказа: {product_list_str}."
        )
        self.mail.send(msg)

    def register_routes(self):
        @self.route('/place_order', methods=['POST'])
        def place_order():
            name = request.json.get('name', '')
            city = request.json.get('city', '')
            address = request.json.get('address', '')
            email = request.json.get('email', '')

            basket = request.json.get('basket', [])
            product_titles = [item['title'] for item in basket]
            product_list_str = ', '.join(product_titles)

            self.order_facade.place_order(name, city, address, email, product_list_str)
            session.pop('basket', None) 
            return "Заказ успешно оформлен", 200

if __name__ == '__main__':
    app_instance = NotificationService(__name__)
    app_instance.run(debug=True, host='0.0.0.0')