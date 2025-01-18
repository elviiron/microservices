import unittest
from unittest.mock import patch
from app import App


class TestApp(unittest.TestCase):

    @patch('flask_mail.Mail.send')
    def setUp(self, mock_send):
        self.app = App(__name__)
        self.mock_send = mock_send

    @patch('flask_mail.Mail.send')
    def test_send_order_confirmation(self, mock_send):
        email = "elvi2004@gmail.com"
        name = "Эльвира"
        address = "ул.Петропавловская, 11"
        city = "г.Пермь"
        product_list_str = "INSPIRE САРАФАН ДЛИНЫ МИДИ С ЗАВЯЗКАМИ НА СПИНЕ (БЕЛЫЙ)"

        with self.app.app_context():
            self.app.send_order_confirmation(email, name, address, city, product_list_str)

            msg = mock_send.call_args[0][0]
            self.assertEqual(msg.subject, "Заказ оформлен")
            self.assertEqual(msg.recipients, [email])
            self.assertEqual(msg.body, (
                f"Спасибо за ваш заказ, {name}! "
                f"Ваш адрес: {address}, {city}. "
                f"Содержимое заказа: {product_list_str}."
            ))


if __name__ == '__main__':
    unittest.main()



