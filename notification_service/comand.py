

class PlaceOrderComand:
    def __init__(self, order_repo, email_service):
        self.order_repo = order_repo
        self.email_service = email_service

    def execute(self, name, city, address, email, product_list_str):
        self.order_repo.insert_order(name, city, address, email, product_list_str)

        self.email_service.send_order_confirmation(email, name + "1", address, city, product_list_str)